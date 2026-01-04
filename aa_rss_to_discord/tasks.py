"""
AA RSS To Discord Tasks
"""

# Standard Library
import re

# Third Party
import feedparser
from aadiscordbot.tasks import send_message
from celery import group, shared_task

# Alliance Auth
from allianceauth.services.hooks import get_extension_logger
from allianceauth.services.tasks import QueueOnce

# AA RSS to Discord
from aa_rss_to_discord import __title__
from aa_rss_to_discord.constants import USER_AGENT
from aa_rss_to_discord.models import LastItem, RssFeeds
from aa_rss_to_discord.providers import AppLogger

logger = AppLogger(get_extension_logger(__name__), __title__)


def remove_emoji(string: str) -> str:
    """
    Removing these dumb as fuck emojis from the title string.
    Like honestly, who in the hell needs that shit?

    :param string: Input string
    :type string: str
    :return: String without emojis
    :rtype: str
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
    Fetch all enabled RSS feeds and dispatch processing tasks.

    :return: None
    :rtype: None
    """

    rss_feeds = RssFeeds.objects.select_enabled()
    if not rss_feeds:
        logger.debug("No RSS feeds found to parse.")
        return

    feed_ids = [f.id for f in rss_feeds]
    if not feed_ids:
        logger.debug("No RSS feed ids to dispatch.")
        return

    group(_process_feed.s(fid) for fid in feed_ids).apply_async()


@shared_task
def _process_feed(rss_feed_id: int) -> None:
    """
    Process a single RSS feed by fetching its latest entry and posting to Discord if it's new.

    :param rss_feed_id: ID of the RSS feed to process
    :type rss_feed_id: int
    :return: None
    :rtype: None
    """

    try:
        rss_feed = RssFeeds.objects.select_related("discord_channel").get(
            id=rss_feed_id
        )
    except RssFeeds.DoesNotExist:
        logger.debug("RSS feed %s not found", rss_feed_id)
        return

    logger.info(f'Fetching RSS Feed "{rss_feed.name}"')
    feed = feedparser.parse(rss_feed.url, agent=USER_AGENT)

    latest_entry = next(iter(getattr(feed, "entries", [])), None)
    if not latest_entry:
        logger.debug(f'No entries found for feed "{rss_feed.name}".')
        return

    feed_entry_title = remove_emoji(latest_entry.get("title", "No title"))
    feed_entry_link = latest_entry.get("link")
    feed_entry_time = latest_entry.get("published", latest_entry.get("updated"))
    feed_entry_guid = latest_entry.get("id")

    last_item = LastItem.objects.filter(rss_feed=rss_feed).first()
    if last_item and (
        last_item.rss_item_time,
        last_item.rss_item_title,
        last_item.rss_item_link,
        last_item.rss_item_guid,
    ) == (feed_entry_time, feed_entry_title, feed_entry_link, feed_entry_guid):
        logger.debug(
            'News item "%s" for RSS Feed "%s" has already been posted to your Discord',
            feed_entry_title,
            rss_feed.name,
        )
        return

    if not last_item:
        logger.debug("This seems to be a completely new RSS feed: %s", rss_feed.name)

    logger.info(
        'New entry found for RSS feed "%s", posting to Discord channel %s',
        rss_feed.name,
        rss_feed.discord_channel,
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
