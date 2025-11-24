# Third Party
from aadiscordbot.models import Channels, Servers

# AA RSS to Discord
from aa_rss_to_discord.models import LastItem, RssFeeds
from aa_rss_to_discord.tests import BaseTestCase


class TestRssFeeds(BaseTestCase):
    """
    Test the RssFeeds model.
    """

    def test_saves_and_retrieves_rss_feed_correctly(self):
        """
        Tests that an RSS feed can be saved and retrieved correctly.

        :return:
        :rtype:
        """

        feed = RssFeeds.objects.create(
            name="Feed 1", url="http://example.com/rss", enabled=True
        )
        retrieved_feed = RssFeeds.objects.get(id=feed.id)

        self.assertEqual(retrieved_feed.name, "Feed 1")
        self.assertEqual(retrieved_feed.url, "http://example.com/rss")
        self.assertTrue(retrieved_feed.enabled)

    def test_handles_null_discord_channel_gracefully(self):
        """
        Tests that the model handles a null discord_channel gracefully.

        :return:
        :rtype:
        """

        feed = RssFeeds.objects.create(
            name="Feed 2", url="http://example.com/rss", discord_channel=None
        )

        self.assertIsNone(feed.discord_channel)

    def test_string_representation_includes_name_and_channel(self):
        """
        Tests that the string representation of the RssFeeds model

        :return:
        :rtype:
        """
        server = Servers.objects.create(server=1, name="Test Server")
        channel = Channels.objects.create(name="General", server=server, channel=1)
        feed = RssFeeds.objects.create(name="Feed 3", discord_channel=channel)

        self.assertEqual(
            str(feed), 'RSS Feed "Feed 3" for channel "General" On "Test Server"'
        )

    def test_allows_disabling_rss_feed(self):
        """
        Tests that an RSS feed can be disabled.

        :return:
        :rtype:
        """
        feed = RssFeeds.objects.create(name="Feed 4", enabled=True)
        feed.enabled = False
        feed.save()

        updated_feed = RssFeeds.objects.get(id=feed.id)

        self.assertFalse(updated_feed.enabled)

    def test_handles_empty_name_and_url_gracefully(self):
        """
        Tests that the model handles empty name and url fields gracefully.

        :return:
        :rtype:
        """

        feed = RssFeeds.objects.create(name="", url="")

        self.assertEqual(feed.name, "")
        self.assertEqual(feed.url, "")


class TestLastItem(BaseTestCase):
    """
    Test the LastItem model.
    """

    def test_string_representation_includes_item_title(self):
        """
        Tests that the string representation of the LastItem model includes the item title.

        :return:
        :rtype:
        """

        feed = RssFeeds.objects.create(name="Feed 1", url="http://example.com/rss")
        item = LastItem.objects.create(
            rss_feed=feed,
            rss_item_title="Sample Item",
            rss_item_link="http://example.com/item",
        )

        self.assertEqual(str(item), 'RSS Entry "Sample Item"')

    def test_handles_empty_item_title_gracefully(self):
        """
        Tests that the model handles an empty item title gracefully.

        :return:
        :rtype:
        """

        feed = RssFeeds.objects.create(name="Feed 2", url="http://example.com/rss")
        item = LastItem.objects.create(
            rss_feed=feed,
            rss_item_title="",
            rss_item_link="http://example.com/item",
        )

        self.assertEqual(str(item), 'RSS Entry ""')

    def test_saves_and_retrieves_last_item_correctly(self):
        """
        Tests that a LastItem can be saved and retrieved correctly.

        :return:
        :rtype:
        """

        feed = RssFeeds.objects.create(name="Feed 3", url="http://example.com/rss")
        item = LastItem.objects.create(
            rss_feed=feed,
            rss_item_time="2023-10-01T12:00:00Z",
            rss_item_title="Item Title",
            rss_item_link="http://example.com/item",
            rss_item_guid="12345",
        )
        retrieved_item = LastItem.objects.get(id=item.id)

        self.assertEqual(retrieved_item.rss_item_time, "2023-10-01T12:00:00Z")
        self.assertEqual(retrieved_item.rss_item_title, "Item Title")
        self.assertEqual(retrieved_item.rss_item_link, "http://example.com/item")
        self.assertEqual(retrieved_item.rss_item_guid, "12345")

    def test_handles_null_guid_gracefully(self):
        """
        Tests that the model handles a null guid gracefully.

        :return:
        :rtype:
        """

        feed = RssFeeds.objects.create(name="Feed 4", url="http://example.com/rss")
        item = LastItem.objects.create(
            rss_feed=feed,
            rss_item_guid="",
        )

        self.assertEqual(item.rss_item_guid, "")
