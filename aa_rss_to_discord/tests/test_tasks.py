"""
Test cases for the fetch_rss task
"""

# Standard Library
from unittest.mock import MagicMock, patch

# AA RSS to Discord
from aa_rss_to_discord.models import LastItem
from aa_rss_to_discord.tasks import fetch_rss
from aa_rss_to_discord.tests import BaseTestCase


class TestFetchRss(BaseTestCase):
    """
    Test fetch_rss task
    """

    def test_logs_warning_if_no_rss_feeds_found(self):
        """
        Test that a warning is logged if no RSS feeds are found.

        :return:
        :rtype:
        """

        with (
            patch(
                "aa_rss_to_discord.tasks.RssFeeds.objects.select_enabled",
                return_value=[],
            ),
            patch("aa_rss_to_discord.tasks.logger.debug") as mock_debug,
        ):
            fetch_rss()
            mock_debug.assert_called_once_with("No RSS feeds found to parse.")

    def test_processes_valid_rss_feed_entry(self):
        """
        Test that a valid RSS feed entry is processed and sent to Discord.

        :return:
        :rtype:
        """

        discord_channel = MagicMock()
        discord_channel.channel = 12345

        rss_feed = MagicMock()
        rss_feed.name = "Valid Feed"
        rss_feed.url = "http://example.com/rss"
        rss_feed.discord_channel = discord_channel

        # Use a MagicMock that acts like feedparser entry with both dict and attribute access
        feed_entry = MagicMock()
        feed_entry.get = lambda key, default=None: {
            "title": "Valid Entry",
            "link": "http://example.com/valid-entry",
            "published": "2023-10-01T12:00:00Z",
            "id": "entry-1",
        }.get(key, default)
        feed_entry.updated = (
            "2023-10-01T12:00:00Z"  # Fallback if 'published' is missing
        )

        parsed_feed = MagicMock()
        parsed_feed.entries = [feed_entry]

        with (
            patch(
                "aa_rss_to_discord.tasks.RssFeeds.objects.select_enabled",
                return_value=[rss_feed],
            ),
            patch(
                "aa_rss_to_discord.tasks.feedparser.parse",
                return_value=parsed_feed,
            ),
            patch(
                "aa_rss_to_discord.tasks.LastItem.objects.get",
                side_effect=LastItem.DoesNotExist,
            ),
            patch(
                "aa_rss_to_discord.tasks.LastItem.objects.update_or_create",
            ),
            patch(
                "aa_rss_to_discord.tasks.send_message",
            ) as mock_send_message,
        ):
            fetch_rss()

            mock_send_message.assert_called_once()
            call_args = mock_send_message.call_args
            self.assertEqual(call_args.kwargs.get("channel_id"), 12345)
            message = call_args.kwargs.get("message", "")
            self.assertIn("http://example.com/valid-entry", message)
            self.assertIn("Valid Feed", message)

    def test_skips_duplicate_rss_feed_entry(self):
        """
        Test that a duplicate RSS feed entry is skipped.

        :return:
        :rtype:
        """

        rss_feed = MagicMock()
        rss_feed.name = "Duplicate Feed"
        rss_feed.url = "http://example.com/rss"

        # Create feed entry that supports both dict-style and attribute access
        feed_entry = MagicMock()
        feed_entry.get = lambda key, default=None: {
            "title": "Duplicate Entry",
            "link": "http://example.com/duplicate-entry",
            "published": "2023-10-01T12:00:00Z",
            "id": "entry-1",
        }.get(key, default)
        feed_entry.updated = "2023-10-01T12:00:00Z"

        last_item = MagicMock(
            rss_item_time="2023-10-01T12:00:00Z",
            rss_item_title="Duplicate Entry",
            rss_item_link="http://example.com/duplicate-entry",
            rss_item_guid="entry-1",
        )

        with (
            patch(
                "aa_rss_to_discord.tasks.RssFeeds.objects.select_enabled",
                return_value=[rss_feed],
            ),
            patch(
                "aa_rss_to_discord.tasks.feedparser.parse",
                return_value=MagicMock(entries=[feed_entry]),
            ),
            patch(
                "aa_rss_to_discord.tasks.LastItem.objects.get",
                return_value=last_item,
            ),
            patch("aa_rss_to_discord.tasks.logger.debug") as mock_debug,
            patch("aa_rss_to_discord.tasks.send_message") as mock_send_message,
        ):
            fetch_rss()

            mock_send_message.assert_not_called()
            mock_debug.assert_any_call(
                'News item "Duplicate Entry" for RSS Feed "Duplicate Feed" has already been posted to your Discord'
            )

    def test_skips_rss_feed_with_no_entries(self):
        """
        Test that an RSS feed with no entries is skipped.

        :return:
        :rtype:
        """

        rss_feed = MagicMock()
        rss_feed.name = "Empty Feed"
        rss_feed.url = "http://example.com/rss"

        with (
            patch(
                "aa_rss_to_discord.tasks.RssFeeds.objects.select_enabled",
                return_value=[rss_feed],
            ),
            patch(
                "aa_rss_to_discord.tasks.feedparser.parse",
                return_value=MagicMock(entries=[]),
            ),
            patch("aa_rss_to_discord.tasks.logger.debug") as mock_debug,
        ):
            fetch_rss()

            mock_debug.assert_any_call(
                'Error processing feed "Empty Feed": list index out of range'
            )
