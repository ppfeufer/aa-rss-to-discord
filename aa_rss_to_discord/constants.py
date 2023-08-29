"""
constants
"""

# Django
from django.utils.text import slugify

# AA RSS to Discord
from aa_rss_to_discord import __version__

VERBOSE_NAME = (
    "AA RSS To Discord - Alliance Auth "
    "module to post news from RSS feeds to your Discord"
)

verbose_name_slugified: str = slugify(VERBOSE_NAME, allow_unicode=True)
github_url: str = "https://github.com/ppfeufer/aa-rss-to-discord"
USER_AGENT = f"{verbose_name_slugified} v{__version__} {github_url}"
