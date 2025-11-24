# AA RSS to Discord
from aa_rss_to_discord.models import RssFeeds
from aa_rss_to_discord.tests import BaseTestCase


class TestRssFeedManager(BaseTestCase):
    """
    Test the RSS Feed Manager
    """

    def test_returns_only_enabled_feeds(self):
        RssFeeds.objects.create(name="Feed 1", enabled=True)
        RssFeeds.objects.create(name="Feed 2", enabled=False)
        RssFeeds.objects.create(name="Feed 3", enabled=True)

        result = RssFeeds.objects.select_enabled()

        self.assertEqual(result.count(), 2)
        self.assertTrue(all(feed.enabled for feed in result))

    def test_handles_no_enabled_feeds_gracefully(self):
        RssFeeds.objects.create(name="Feed 1", enabled=False)
        RssFeeds.objects.create(name="Feed 2", enabled=False)

        result = RssFeeds.objects.select_enabled()

        self.assertEqual(result.count(), 0)

    def test_handles_empty_database_gracefully(self):
        result = RssFeeds.objects.select_enabled()

        self.assertEqual(result.count(), 0)
