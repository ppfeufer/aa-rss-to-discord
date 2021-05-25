"""
Our Models
"""

from aadiscordbot.models import Channels

from django.db import models
from django.utils.translation import gettext as _

from aa_rss_to_discord.managers import RssFeedsManager


class RssFeeds(models.Model):
    """
    Model :: RssFeeds
    """

    name = models.CharField(max_length=254, default="")
    url = models.CharField(max_length=254, default="")
    discord_channel = models.ForeignKey(
        Channels,
        related_name="+",
        null=True,
        blank=True,
        default=None,
        on_delete=models.SET_NULL,
    )
    enabled = models.BooleanField(default=True)

    objects = RssFeedsManager()

    class Meta:
        """
        Meta definitions
        """

        default_permissions = ()
        verbose_name = _("RSS Feed")
        verbose_name_plural = _("RSS Feeds")

    def __str__(self):
        return f'RSS Feed "{self.name}" for channel {self.discord_channel}'

    def get_last_item(self):
        """
        Get the last item for this RSS feed from DB
        :return:
        :rtype:
        """

        return LastItem.objects.get(rss_feed=self)

    def set_last_item(self, time, title, link, guid):
        """
        Set the last item for this RSS feed
        :param time:
        :type time:
        :param title:
        :type title:
        :param link:
        :type link:
        :param guid:
        :type guid:
        """

        LastItem(
            rss_feed=self,
            rss_item_time=time,
            rss_item_title=title,
            rss_item_link=link,
            rss_item_guid=guid,
        ).save()

    def remove_last_item(self):
        """
        Remove the last item for this RSS feed
        """

        LastItem.objects.filter(rss_feed=self).delete()


class LastItem(models.Model):
    """
    Model :: LastItem
    """

    rss_feed = models.ForeignKey(
        RssFeeds,
        related_name="+",
        on_delete=models.CASCADE,
    )
    rss_item_time = models.CharField(max_length=254, blank=True, default="")
    rss_item_title = models.CharField(max_length=254, default="")
    rss_item_link = models.CharField(max_length=254, default="")
    rss_item_guid = models.CharField(max_length=254, blank=True, default="")

    class Meta:
        """
        Meta definitions
        """

        default_permissions = ()
        verbose_name = _("Last Item")
        verbose_name_plural = _("Last Items")

    def __str__(self):
        return f'RSS Entry "{self.rss_item_title}"'
