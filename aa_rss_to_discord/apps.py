"""
app config
"""

# Django
from django.apps import AppConfig
from django.utils.text import format_lazy

# AA RSS to Discord
from aa_rss_to_discord import __title_translated__, __version__


class AaRssToDiscordConfig(AppConfig):
    """
    application config
    """

    name = "aa_rss_to_discord"
    label = "aa_rss_to_discord"
    verbose_name = format_lazy(
        "{app_title} v{version}", app_title=__title_translated__, version=__version__
    )
