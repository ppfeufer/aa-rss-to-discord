"""
AA RSS To Discord Tasks
"""

# Standard Library
import re

# Third Party
import feedparser
from aadiscordbot.tasks import send_message
from celery import shared_task

# Alliance Auth
from allianceauth.services.hooks import get_extension_logger
from allianceauth.services.tasks import QueueOnce

# AA RSS to Discord
from aa_rss_to_discord import __title__
from aa_rss_to_discord.constants import USER_AGENT
from aa_rss_to_discord.models import LastItem, RssFeeds
from aa_rss_to_discord.providers import AppLogger

logger = AppLogger(get_extension_logger(__name__), __title__)


def remove_emoji(string):
    """
    Removing these dumb as fuck emojis from the title string.
    Like honestly, who in the hell needs that shit?

    :param string:
    :type string:
    :return:
    :rtype:
    """

    emoji_pattern = re.compile(
        pattern="["
        "\U0001f600-\U0001f64f"  # Emoticons
        "\U0001f300-\U0001f5ff"  # Symbols & pictographs
        "\U0001f680-\U0001f6ff"  # Transport & map symbols
        "\U0001f1e0-\U0001f1ff"  # Flags (iOS)
        "\U00002500-\U00002bef"  # Chinese char
        "\U00002702-\U000027b0"
        "\U00002702-\U000027b0"
        "\U000024c2-\U0001f251"
        "\U0001f926-\U0001f937"
        "\U00010000-\U0010ffff"
        "\u2640-\u2642"
        "\u2600-\u2b55"
        "\u200d"
        "\u23cf"
        "\u23e9"
        "\u231a"
        "\ufe0f"  # Dingbats
        "\u3030"
        "]+",
        flags=re.UNICODE,
    )

    return emoji_pattern.sub(repl=r"", string=string)


@shared_task(**{"base": QueueOnce})
def fetch_rss() -> None:
    """
    Fetch RSS feeds and post new entries to Discord channels.

    :return:
    :rtype:
    """

    rss_feeds = RssFeeds.objects.select_enabled()

    if not rss_feeds:
        logger.debug("No RSS feeds found to parse.")

        return

    for rss_feed in rss_feeds:
        logger.info(f'Fetching RSS Feed "{rss_feed.name}"')
        feed = feedparser.parse(rss_feed.url, agent=USER_AGENT)

        try:
            latest_entry = feed.entries[0]
            feed_entry_title = remove_emoji(latest_entry.get("title", "No title"))
            feed_entry_link = latest_entry.get("link")
            feed_entry_time = latest_entry.get("published", latest_entry.updated)
            feed_entry_guid = latest_entry.get("id")
        except (AttributeError, IndexError) as exc:
            logger.debug(f'Error processing feed "{rss_feed.name}": {exc}')

            continue

        try:
            last_item = LastItem.objects.get(rss_feed=rss_feed)
            is_duplicate = (
                last_item.rss_item_time == feed_entry_time
                and last_item.rss_item_title == feed_entry_title
                and last_item.rss_item_link == feed_entry_link
                and last_item.rss_item_guid == feed_entry_guid
            )

            if is_duplicate:
                logger.debug(
                    f'News item "{feed_entry_title}" for RSS Feed "{rss_feed.name}" '
                    "has already been posted to your Discord"
                )

                continue
        except LastItem.DoesNotExist:
            logger.debug("This seems to be a completely new RSS feed.")

        logger.info(
            f"New entry found, posting to Discord channel {rss_feed.discord_channel}"
        )

        LastItem.objects.update_or_create(
            rss_feed=rss_feed,
            defaults={
                "rss_item_time": feed_entry_time,
                "rss_item_title": feed_entry_title,
                "rss_item_link": feed_entry_link,
                "rss_item_guid": feed_entry_guid,
            },
        )

        send_message(
            channel_id=rss_feed.discord_channel.channel,
            message=f"**{rss_feed.name}**\n{feed_entry_link}",
        )
