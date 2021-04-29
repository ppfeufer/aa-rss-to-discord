"""
Django admin declarations
"""

from django.contrib import admin

from aa_rss_to_discord.models import RssFeeds


def custom_filter(title):
    """
    custom filter for model properties
    :param title:
    :return:
    """

    class Wrapper(admin.FieldListFilter):
        """
        custom_filter :: wrapper
        """

        def __new__(cls, *args, **kwargs):
            instance = admin.FieldListFilter.create(*args, **kwargs)
            instance.title = title

            return instance

    return Wrapper


@admin.register(RssFeeds)
class RssFeedsAdmin(admin.ModelAdmin):
    """
    RssFeedsAdmin
    """

    list_display = ("name", "url", "discord_channel")
    ordering = ("name",)

    list_filter = ("name", "url", "discord_channel")

    search_fields = ("name", "url", "discord_channel")
