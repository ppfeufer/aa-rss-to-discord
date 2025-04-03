"""
"RSS" cog for discordbot - https://github.com/pvyParts/allianceauth-discordbot
"""

# Standard Library
import logging

# Third Party
from aadiscordbot import app_settings
from aadiscordbot.models import Channels, Servers
from discord.commands import SlashCommandGroup, option
from discord.ext import commands

# Django
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator

# AA RSS to Discord
from aa_rss_to_discord.models import RssFeeds

logger = logging.getLogger(__name__)


class Rss(commands.Cog):
    """
    RSS management via Discord
    """

    def __init__(self, bot):
        self.bot = bot

    admin_commands = SlashCommandGroup(
        "rss", "RSS Admin Commands", guild_ids=app_settings.get_all_servers()
    )

    @admin_commands.command(name="add", guild_ids=app_settings.get_all_servers())
    @option("rss_url", description="The URL to the RSS/Atom feed")
    @option("rss_name", description="A descriptive name for the RSS/Atom feed")
    async def rss_add(self, ctx, rss_url: str, rss_name: str):
        """
        Adding an RSS/Atom feed to the current Discord channel
        """

        await ctx.trigger_typing()

        if ctx.author.id not in app_settings.get_admins():
            return await ctx.respond(
                "You do not have permission to use this command",
                ephemeral=True,
            )

        if rss_url is None or rss_name is None:
            return await ctx.respond(
                (
                    "To add a RSS/Atom feed to this channel, "
                    "please use the following syntax.\n\n"
                    "```/rss add rss_url rss_name```\n\n"
                    "Both arguments are required."
                ),
                ephemeral=True,
            )

        channel_name = ctx.channel.name
        channel_id = ctx.channel.id
        server_name = ctx.guild.name
        server_id = ctx.guild.id

        validate_url = URLValidator()

        # Check if rss_url is a valid URL
        try:
            validate_url(rss_url)
        except ValidationError:
            return await ctx.respond("The URL provided is not valid!", ephemeral=True)

        # Check if there is already a RSS/Atom feed with this URL for this channel
        if RssFeeds.objects.filter(
            url__iexact=rss_url, discord_channel_id__exact=channel_id
        ).exists():
            return await ctx.respond(
                "A RSS/Atom feed with this URL already exists for this channel",
                ephemeral=True,
            )

        # Check if the current server and channel are already
        # known to the allianceauth-discordbot module
        if not Servers.objects.filter(server__exact=server_id).exists():
            Servers(server=server_id, name=server_name).save()

        if not Channels.objects.filter(
            channel__exact=channel_id, server_id__exact=server_id
        ).exists():
            Channels(channel=channel_id, name=channel_name, server_id=server_id).save()

        # Add the new RSS/Atom feed
        RssFeeds(
            url=rss_url, name=rss_name, discord_channel_id=channel_id, enabled=True
        ).save()

        return await ctx.respond(
            f'RSS/Atom feed "{rss_name}" added to this channel', ephemeral=True
        )

    @admin_commands.command(name="list", guild_ids=app_settings.get_all_servers())
    async def rss_list(self, ctx):
        """
        List all RSS/Atom feeds for the current Discord channel
        """

        await ctx.trigger_typing()

        if ctx.author.id not in app_settings.get_admins():
            return await ctx.respond(
                "You do not have permission to use this command",
                ephemeral=True,
            )

        channel_id = ctx.channel.id
        payload = "No RSS/Atom feeds have been registered for this channel."
        rss_feeds = RssFeeds.objects.filter(discord_channel_id__exact=channel_id)

        if rss_feeds.count() > 0:
            payload = (
                "The following RSS/Atom feeds are registered for this channel:\n\n```"
            )

            for rss_feed in rss_feeds:
                rss_status = "Enabled" if rss_feed.enabled is True else "Disabled"

                payload += (
                    f"ID: {rss_feed.pk}\n"
                    f"Name: {rss_feed.name}\n"
                    f"URL: {rss_feed.url}\n"
                    f"Status: {rss_status}\n\n"
                )

            payload += "```"

        return await ctx.respond(payload, ephemeral=True)

    @admin_commands.command(name="delete", guild_ids=app_settings.get_all_servers())
    @option(
        "rss_feed_id",
        description="The ID of the RSS/Atom feed to delete. (Get it from the list command)",
    )
    async def rss_delete(self, ctx, rss_feed_id: int):
        """
        Remove an RSS/Atom feed from the current Discord channel
        """

        await ctx.trigger_typing()

        if ctx.author.id not in app_settings.get_admins():
            return await ctx.respond(
                "You do not have permission to use this command",
                ephemeral=True,
            )

        channel_id = ctx.channel.id

        try:
            rss_feed = RssFeeds.objects.get(
                pk=rss_feed_id, discord_channel_id__exact=channel_id
            )

            rss_feed_name = rss_feed.name

            rss_feed.delete()

            payload = (
                f'RSS/Atom feed "{rss_feed_name}" has been removed from this channel.'
            )
        except RssFeeds.DoesNotExist:
            payload = "This RSS/Atom feed does not exist in this Discord channel."

        return await ctx.respond(payload, ephemeral=True)

    @admin_commands.command(name="enable", guild_ids=app_settings.get_all_servers())
    @option(
        "rss_feed_id",
        description="The ID of the RSS/Atom feed to delete. (Get it from the list command)",
    )
    async def rss_enable(self, ctx, rss_feed_id: int):
        """
        Enable a disabled RSS/Atom feed for the current Discord channel
        """

        await ctx.trigger_typing()

        if ctx.author.id not in app_settings.get_admins():
            return await ctx.respond(
                "You do not have permission to use this command",
                ephemeral=True,
            )

        channel_id = ctx.channel.id

        try:
            rss_feed = RssFeeds.objects.get(
                pk=rss_feed_id, discord_channel_id__exact=channel_id
            )

            rss_feed.enabled = 1
            rss_feed.save()

            payload = (
                f'RSS/Atom feed "{rss_feed.name}" has been enabled for this channel.'
            )
        except RssFeeds.DoesNotExist:
            payload = "This RSS/Atom feed does not exist in this Discord channel."

        return await ctx.respond(payload, ephemeral=True)

    @admin_commands.command(name="disable", guild_ids=app_settings.get_all_servers())
    @option(
        "rss_feed_id",
        description="The ID of the RSS/Atom feed to delete. (Get it from the list command)",
    )
    async def rss_disable(self, ctx, rss_feed_id: int):
        """
        Disable an enabled RSS/Atom feed for the current Discord channel
        """

        await ctx.trigger_typing()

        if ctx.author.id not in app_settings.get_admins():
            return await ctx.respond(
                "You do not have permission to use this command",
                ephemeral=True,
            )

        channel_id = ctx.channel.id

        try:
            rss_feed = RssFeeds.objects.get(
                pk=rss_feed_id, discord_channel_id__exact=channel_id
            )

            rss_feed.enabled = 0
            rss_feed.save()

            payload = (
                f'RSS/Atom feed "{rss_feed.name}" has been disabled for this channel.'
            )
        except RssFeeds.DoesNotExist:
            payload = "This RSS/Atom feed does not exist in this Discord channel."

        return await ctx.respond(payload, ephemeral=True)


def setup(bot):
    """
    Setup the cog
    :param bot:
    """

    bot.add_cog(Rss(bot))
