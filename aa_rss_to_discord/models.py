"""
Our Models
"""

from aadiscordbot.models import Channels

from django.db import models
from django.utils.translation import gettext as _


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

    class Meta:
        """
        Meta definitions
        """

        default_permissions = ()
        verbose_name = _("RSS Feed")
        verbose_name_plural = _("RSS Feeds")

    def __str__(self):
        return f'RSS Feed "{self.name}" for channel {self.discord_channel}'
