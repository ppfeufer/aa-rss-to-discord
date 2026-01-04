"""
Test cases for the fetch_rss task
"""

# Standard Library
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

# AA RSS to Discord
from aa_rss_to_discord.constants import USER_AGENT
from aa_rss_to_discord.models import RssFeeds
from aa_rss_to_discord.tasks import _process_feed, fetch_rss
from aa_rss_to_discord.tests import BaseTestCase


class TestFetchRss(BaseTestCase):
    """
    Test cases for the fetch_rss task
    """

    def test_fetch_rss_logs_message_when_no_rss_feeds_found(self):
        """
        Test that fetch_rss logs a message when no RSS feeds are found.

        :return:
        :rtype:
        """

        with (
            patch(
                "aa_rss_to_discord.tasks.RssFeeds.objects.select_enabled"
            ) as mock_select_enabled,
            patch("aa_rss_to_discord.tasks.logger.debug") as mock_logger_debug,
        ):
            mock_select_enabled.return_value = []

            fetch_rss()

            mock_logger_debug.assert_called_once_with("No RSS feeds found to parse.")

    def test_fetch_rss_dispatches_tasks_for_enabled_feeds(self):
        """
        Test that fetch_rss dispatches tasks for enabled RSS feeds.

        :return:
        :rtype:
        """

        with (
            patch(
                "aa_rss_to_discord.tasks.RssFeeds.objects.select_enabled"
            ) as mock_select_enabled,
            patch("aa_rss_to_discord.tasks.group") as mock_group,
        ):
            mock_rss_feed_1 = MagicMock(id=1)
            mock_rss_feed_2 = MagicMock(id=2)
            mock_select_enabled.return_value = [mock_rss_feed_1, mock_rss_feed_2]

            fetch_rss()

            mock_group.assert_called_once()
            mock_group.return_value.apply_async.assert_called_once()
            dispatched_tasks = mock_group.call_args[0][0]
            dispatched_list = list(dispatched_tasks)
            self.assertEqual(len(dispatched_list), 2)
            self.assertEqual(dispatched_list[0].args[0], 1)
            self.assertEqual(dispatched_list[1].args[0], 2)

    def test_handles_empty_rss_feed_ids_gracefully(self):
        """
        Test that fetch_rss handles an empty list of RSS feed IDs gracefully.

        :return:
        :rtype:
        """

        with (
            patch(
                "aa_rss_to_discord.tasks.RssFeeds.objects.select_enabled"
            ) as mock_select_enabled,
            patch("aa_rss_to_discord.tasks.group") as mock_group,
            patch("aa_rss_to_discord.tasks.logger.debug") as mock_logger_debug,
        ):
            mock_select_enabled.return_value = iter([])

            fetch_rss()

            mock_group.assert_not_called()
            mock_logger_debug.assert_called_once_with("No RSS feed ids to dispatch.")


class TestHelperProcessRssFeed(BaseTestCase):
    """
    Test cases for the _process_feed task
    """

    def test_handles_missing_rss_feed_gracefully(self):
        """
        Test that _process_feed handles a missing RSS feed gracefully.

        :return:
        :rtype:
        """

        with patch(
            "aa_rss_to_discord.tasks.RssFeeds.objects.select_related"
        ) as mock_select_related:
            mock_select_related.return_value.get.side_effect = RssFeeds.DoesNotExist

            _process_feed(1)

            mock_select_related.return_value.get.assert_called_once_with(id=1)

    def test_logs_and_skips_when_no_entries_in_feed(self):
        """
        Test that _process_feed logs and skips processing when no entries are found in the feed.

        :return:
        :rtype:
        """

        with (
            patch(
                "aa_rss_to_discord.tasks.RssFeeds.objects.select_related"
            ) as mock_select_related,
            patch(
                "aa_rss_to_discord.tasks.feedparser.parse", return_value={}
            ) as mock_parse,
        ):
            mock_rss_feed = MagicMock(url="http://example.com", name="No Entries Feed")
            mock_select_related.return_value.get.return_value = mock_rss_feed

            _process_feed(1)

            mock_parse.assert_called_once_with(mock_rss_feed.url, agent=USER_AGENT)

    def test_posts_new_entry_to_discord(self):
        """
        Test that _process_feed posts a new entry to Discord when it's not a duplicate.

        :return:
        :rtype:
        """

        entry = {"title": "New Entry", "link": "http://example.com", "id": "123"}

        with (
            patch(
                "aa_rss_to_discord.tasks.RssFeeds.objects.select_related"
            ) as mock_select_related,
            patch(
                "aa_rss_to_discord.tasks.feedparser.parse",
                return_value=SimpleNamespace(entries=[entry]),
            ) as mock_parse,
            patch("aa_rss_to_discord.tasks.LastItem.objects.filter") as mock_filter,
            patch(
                "aa_rss_to_discord.tasks.LastItem.objects.update_or_create"
            ) as mock_update_or_create,
            patch("aa_rss_to_discord.tasks.send_message") as mock_send_message,
        ):
            mock_rss_feed = MagicMock(
                discord_channel=MagicMock(channel=12345),
                name="Test Feed",
                url="http://example.com",
            )
            mock_select_related.return_value.get.return_value = mock_rss_feed
            mock_filter.return_value.first.return_value = None
            mock_update_or_create.return_value = (MagicMock(), True)

            _process_feed(1)

            mock_parse.assert_called_once_with(mock_rss_feed.url, agent=USER_AGENT)
            mock_update_or_create.assert_called_once()
            self.assertTrue(
                mock_send_message.called,
                f"send_message not called. calls: {mock_send_message.call_args_list}",
            )

            call_args, call_kwargs = mock_send_message.call_args
            called_channel = (
                call_kwargs.get("channel_id")
                if "channel_id" in call_kwargs
                else (call_args[0] if len(call_args) > 0 else None)
            )
            called_message = (
                call_kwargs.get("message")
                if "message" in call_kwargs
                else (
                    call_args[1]
                    if len(call_args) > 1
                    else (call_args[0] if len(call_args) == 1 else None)
                )
            )

            self.assertEqual(called_channel, 12345)
            self.assertIsNotNone(called_message)
            self.assertIn(mock_rss_feed.url, called_message)

    def test_skips_posting_duplicate_entry(self):
        """
        Test that _process_feed skips posting a duplicate entry to Discord.

        :return:
        :rtype:
        """

        entry = {"title": "Duplicate Entry", "link": "http://example.com", "id": "123"}

        with (
            patch(
                "aa_rss_to_discord.tasks.RssFeeds.objects.select_related"
            ) as mock_select_related,
            patch(
                "aa_rss_to_discord.tasks.feedparser.parse",
                return_value=SimpleNamespace(entries=[entry]),
            ),
            patch("aa_rss_to_discord.tasks.LastItem.objects.filter") as mock_filter,
            patch("aa_rss_to_discord.tasks.send_message") as mock_send_message,
        ):
            mock_rss_feed = MagicMock(
                discord_channel=MagicMock(channel=12345),
                name="Dup Feed",
                url="http://example.com",
            )
            mock_select_related.return_value.get.return_value = mock_rss_feed
            mock_existing = MagicMock(
                rss_item_time=None,
                rss_item_title="Duplicate Entry",
                rss_item_link="http://example.com",
                rss_item_guid="123",
            )
            mock_filter.return_value.first.return_value = mock_existing

            _process_feed(1)

            mock_send_message.assert_not_called()
