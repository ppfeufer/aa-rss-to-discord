"""
app config
"""

from django.apps import AppConfig

from aa_rss_to_discord import __version__


class AaRssToDiscordConfig(AppConfig):
    """
    application config
    """

    name = "aa_rss_to_discord"
    label = "aa_rss_to_discord"
    verbose_name = f"RSS to Discord v{__version__}"
