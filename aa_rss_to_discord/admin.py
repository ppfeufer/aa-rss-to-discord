"""
Django admin declarations
"""

# Django
from django.contrib import admin

# AA RSS to Discord
from aa_rss_to_discord.models import RssFeeds


@admin.register(RssFeeds)
class RssFeedsAdmin(admin.ModelAdmin):
    """
    RssFeedsAdmin
    """

    list_display = ("name", "enabled", "url", "discord_channel")
    ordering = ("name",)
    list_filter = ("enabled", "discord_channel")
    search_fields = ("name", "url", "discord_channel")
