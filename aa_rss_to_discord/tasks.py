"""
AA RSS To Discord Tasks
"""

import logging
import re

import feedparser
from celery import shared_task

from django.apps import apps

from allianceauth.services.hooks import get_extension_logger
from allianceauth.services.tasks import QueueOnce

from aa_rss_to_discord import __title__
from aa_rss_to_discord.models import RssFeeds
from aa_rss_to_discord.utils import LoggerAddTag

logger = LoggerAddTag(get_extension_logger(__name__), __title__)

# poll every x seconds
RSS_POLL_TIME = 300


def remove_emoji(string):
    """
    removing these dumb as fuck emojis from the title string
    like honestly, who in the hell needs that shit?
    :param string:
    :type string:
    :return:
    :rtype:
    """

    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map symbols
        "\U0001F1E0-\U0001F1FF"  # flags (iOS)
        "\U00002500-\U00002BEF"  # chinese char
        "\U00002702-\U000027B0"
        "\U00002702-\U000027B0"
        "\U000024C2-\U0001F251"
        "\U0001f926-\U0001f937"
        "\U00010000-\U0010ffff"
        "\u2640-\u2642"
        "\u2600-\u2B55"
        "\u200d"
        "\u23cf"
        "\u23e9"
        "\u231a"
        "\ufe0f"  # dingbats
        "\u3030"
        "]+",
        flags=re.UNICODE,
    )

    return emoji_pattern.sub(r"", string)


@shared_task(**{"base": QueueOnce})
def fetch_rss() -> None:
    """
    fetch RSS feeds and post to Discord
    :return:
    :rtype:
    """

    rss_feeds = RssFeeds.objects.select_enabled()

    if apps.is_installed("aadiscordbot") and rss_feeds:
        import aadiscordbot.tasks

        for rss_feed in rss_feeds:
            logger.info(f'Fetching RSS Feed "{rss_feed.name}"')

            feed = feedparser.parse(rss_feed.url)
            latest_entry = feed.entries[0]

            feed_entry_title = remove_emoji(latest_entry.title)
            feed_entry_link = latest_entry.link
            feed_entry_time = latest_entry.get("published", latest_entry.updated)
            feed_entry_guid = latest_entry.id

            post_entry = True

            try:
                last_item = RssFeeds.get_last_item(self=rss_feed)

                if (
                    last_item
                    and last_item.rss_item_time == feed_entry_time
                    and last_item.rss_item_title == feed_entry_title
                    and last_item.rss_item_link == feed_entry_link
                    and last_item.rss_item_guid == feed_entry_guid
                ):
                    logger.info(
                        f'News item "{feed_entry_title}" for RSS Feed '
                        f'"{rss_feed.name}" has already been posted to your Discord'
                    )
                    post_entry = False
            except Exception as e:
                last_item = False
                logger.info(str(e))
                pass

            if post_entry is True:
                logger.info(
                    "New entry found, posting to Discord channel "
                    f"{rss_feed.discord_channel}"
                )

                if last_item is not False:
                    RssFeeds.remove_last_item(self=rss_feed)

                RssFeeds.set_last_item(
                    self=rss_feed,
                    time=feed_entry_time,
                    link=feed_entry_link,
                    title=feed_entry_title,
                    guid=feed_entry_guid,
                )

                discord_message = f"**{rss_feed.name}**\n{feed_entry_link}"

                aadiscordbot.tasks.send_channel_message_by_discord_id.delay(
                    rss_feed.discord_channel.channel,
                    discord_message,
                    embed=False,
                )
    else:
        logging.info(
            "AA Discordbot (https://github.com/pvyParts/allianceauth-discordbot) "
            "needs to be installed and configured."
        )
