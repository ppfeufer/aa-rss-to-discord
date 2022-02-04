"""
Hooking into the auth system
"""

# Alliance Auth
from allianceauth import hooks


@hooks.register("discord_cogs_hook")
def register_cogs():
    """
    Registering our discord cogs
    :return:
    :rtype:
    """

    return ["aa_rss_to_discord.discordbot.cogs.rss"]
