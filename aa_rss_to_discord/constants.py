"""
constants
"""

# Third Party
from feedparser import USER_AGENT as feedparser_user_agent

# AA RSS to Discord
from aa_rss_to_discord import __version__

APP_NAME = "aa-rss-to-discord"
GITHUB_URL = f"https://github.com/ppfeufer/{APP_NAME}"
USER_AGENT = f"{APP_NAME}/{__version__} +{GITHUB_URL} via {feedparser_user_agent}"
