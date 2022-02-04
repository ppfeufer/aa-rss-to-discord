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
USERAGENT = "{verbose_name} v{version} {github_url}".format(
    verbose_name=slugify(VERBOSE_NAME, allow_unicode=True),
    version=__version__,
    github_url="https://github.com/ppfeufer/aa-rss-to-discord",
)
