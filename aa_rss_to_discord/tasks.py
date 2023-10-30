"""
AA RSS To Discord Tasks
"""

# Standard Library
import logging
import re

# Third Party
import feedparser
from celery import shared_task

# Django
from django.apps import apps

# Alliance Auth
from allianceauth.services.hooks import get_extension_logger
from allianceauth.services.tasks import QueueOnce

# Alliance Auth (External Libs)
from app_utils.logging import LoggerAddTag

# AA RSS to Discord
from aa_rss_to_discord import __title__
from aa_rss_to_discord.models import LastItem, RssFeeds

logger = LoggerAddTag(get_extension_logger(__name__), __title__)


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
        "\U0001F600-\U0001F64F"  # Emoticons
        "\U0001F300-\U0001F5FF"  # Symbols & pictographs
        "\U0001F680-\U0001F6FF"  # Transport & map symbols
        "\U0001F1E0-\U0001F1FF"  # Flags (iOS)
        "\U00002500-\U00002BEF"  # Chinese char
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
        "\ufe0f"  # Dingbats
        "\u3030"
        "]+",
        flags=re.UNICODE,
    )

    return emoji_pattern.sub(repl=r"", string=string)


@shared_task(**{"base": QueueOnce})
def fetch_rss() -> None:  # pylint: disable=too-many-statements, too-many-branches
    """
    Fetch RSS feeds and post to Discord

    :return:
    :rtype:
    """

    # pylint: disable=too-many-nested-blocks
    if apps.is_installed(app_name="aadiscordbot"):
        # Third Party
        from aadiscordbot.tasks import (  # pylint: disable=import-outside-toplevel
            send_message,
        )

        rss_feeds = RssFeeds.objects.select_enabled()

        if rss_feeds:
            for rss_feed in rss_feeds:
                logger.info(msg=f'Fetching RSS Feed "{rss_feed.name}"')

                feed = feedparser.parse(url_file_stream_or_string=rss_feed.url)

                feed_entry_title = "No title"
                feed_entry_link = None
                feed_entry_time = None
                feed_entry_guid = None
                has_last_item = False
                last_item = None
                post_entry = False

                try:
                    latest_entry = feed.entries[0]

                    feed_entry_title = remove_emoji(
                        string=latest_entry.get("title", "No title")
                    )
                    feed_entry_link = latest_entry.get("link", None)
                    feed_entry_time = latest_entry.get(
                        "published", latest_entry.updated
                    )
                    feed_entry_guid = latest_entry.get("id", None)
                except AttributeError as exc:
                    logger.debug(
                        msg=f'Malformed RSS feed item in feed "{rss_feed.name}". Error: {exc}'
                    )
                except IndexError as exc:
                    logger.debug(
                        msg=f'Could not index the RSS feed "{rss_feed.name}". Error: {exc}'
                    )
                else:
                    post_entry = True
                    has_last_item = True

                    try:
                        last_item = LastItem.objects.get(rss_feed=rss_feed)

                        if (
                            last_item
                            and last_item.rss_item_time == feed_entry_time
                            and last_item.rss_item_title == feed_entry_title
                            and last_item.rss_item_link == feed_entry_link
                            and last_item.rss_item_guid == feed_entry_guid
                        ):
                            logger.debug(
                                msg=(
                                    f'News item "{feed_entry_title}" for RSS Feed '
                                    f'"{rss_feed.name}" has already been posted to your Discord'
                                )
                            )
                            post_entry = False
                    except LastItem.DoesNotExist:
                        logger.debug(msg="This seems to be a completely new RSS feed.")

                        has_last_item = False

                logger.debug(
                    msg=(
                        "RSS Information gathered: "
                        f"post_entry => {post_entry}, "
                        f'feed_entry_link => "{feed_entry_link}", '
                        f'feed_entry_title => "{feed_entry_title}", '
                        f"feed_entry_time => {feed_entry_time}, "
                        f"feed_entry_guid => {feed_entry_guid}"
                    )
                )

                if (
                    post_entry is True
                    and feed_entry_link is not None
                    and feed_entry_guid is not None
                ):
                    logger.info(
                        msg=(
                            "New entry found, posting to Discord channel "
                            f"{rss_feed.discord_channel}"
                        )
                    )

                    if has_last_item is True:
                        # Update the last item ...
                        last_item.rss_item_time = feed_entry_time
                        last_item.rss_item_title = feed_entry_title
                        last_item.rss_item_link = feed_entry_link
                        last_item.rss_item_guid = feed_entry_guid
                        last_item.save()
                    else:
                        # Set the last item ...
                        LastItem(
                            rss_feed=rss_feed,
                            rss_item_time=feed_entry_time,
                            rss_item_title=feed_entry_title,
                            rss_item_link=feed_entry_link,
                            rss_item_guid=feed_entry_guid,
                        ).save()

                    discord_message = f"**{rss_feed.name}**\n{feed_entry_link}"

                    send_message(
                        channel_id=rss_feed.discord_channel.channel,
                        message=discord_message,
                    )
                else:
                    logger.debug(
                        msg=(
                            f'No item for feed "{rss_feed.name}" to post. '
                            'Missing either "post_entry" to be "True" or '
                            'either "feed_entry_link" or "feed_entry_guid" is "None".'
                        )
                    )
        else:
            logger.debug(msg="No RSS feeds found to parse.")
    else:
        logging.info(
            msg=(
                "AA Discordbot (https://github.com/pvyParts/allianceauth-discordbot) "
                "needs to be installed and configured."
            )
        )
