"""
AA RSS To Discord Tasks
"""

import logging

import feedparser
from celery import shared_task

from django.conf import settings
from django.core.cache import cache
from django.utils.text import slugify

from allianceauth.services.hooks import get_extension_logger
from allianceauth.services.tasks import QueueOnce

from aa_rss_to_discord import __title__
from aa_rss_to_discord.models import RssFeeds
from aa_rss_to_discord.utils import LoggerAddTag

logger = LoggerAddTag(get_extension_logger(__name__), __title__)

# poll every x seconds
RSS_POLL_TIME = 300


@shared_task(**{"base": QueueOnce})
def fetch_rss() -> None:
    """
    fetch RSS feeds and post to Discord
    :return:
    :rtype:
    """

    rss_feeds = RssFeeds.objects.all()

    if "aadiscordbot" in settings.INSTALLED_APPS and rss_feeds:
        import aadiscordbot.tasks

        for rss_feed in rss_feeds:
            try:
                logger.info(f"Fetching RSS Feed {rss_feed.name}")

                rss_cache_key = slugify(rss_feed.url, allow_unicode=True)

                feed = feedparser.parse(rss_feed.url)
                latest_entry = feed.entries[0]
                feed_entry_guid = latest_entry.guid

                if (
                    cache.get(rss_cache_key + "_feed_entry_guid") is None
                    or cache.get(rss_cache_key + "_feed_entry_guid") != feed_entry_guid
                ):
                    post_entry = True

                    # Filter might come later ...
                    # if "filter" in rss_feed:
                    #     if rss_feed.filter in latest_entry.description:
                    #         post_entry = True
                    # else:
                    #     post_entry = True

                    if post_entry is True:
                        logger.info(
                            "New entry found, posting to Discord channel "
                            f'"{rss_feed.discord_channel.channel}"'
                        )

                        feed_title = rss_feed.name
                        feed_entry_link = latest_entry.link

                        discord_message = f"**{feed_title}**\n{feed_entry_link}"

                        aadiscordbot.tasks.send_channel_message_by_discord_id.delay(
                            rss_feed.discord_channel.channel,
                            discord_message,
                            embed=False,
                        )

                        cache.set(
                            rss_cache_key + "_feed_entry_guid", feed_entry_guid, None
                        )
            except Exception as e:
                logger.info(str(e))
                pass
    else:
        logging.info(
            "AA Discordbot (https://github.com/pvyParts/allianceauth-discordbot) "
            "needs to be installed and configured."
        )
