"""
"RSS" cog for discordbot - https://github.com/pvyParts/allianceauth-discordbot
"""

# Standard Library
import logging

# Third Party
import discord
from aadiscordbot.cogs.utils.decorators import sender_is_admin
from aadiscordbot.models import Channels, Servers
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

    @commands.command(pass_context=True)
    @sender_is_admin()
    async def rss_add(self, ctx, rss_url: str = None, *, rss_name: str = None):
        """
        Adding a RSS/Atom feed to the current Discord channel
        """

        await ctx.trigger_typing()

        if rss_url is None or rss_name is None:
            return await ctx.send(
                "To add a RSS/Atom feed to this channel, "
                "please use the following syntax.\n\n"
                "```!rss_add rss_url rss_name```\n\n"
                "Both arguments are required."
            )

        channel_name = ctx.message.channel.name
        channel_id = ctx.message.channel.id
        server_name = ctx.guild.name
        server_id = ctx.guild.id

        validate_url = URLValidator()

        # Check if rss_url is a valid URL
        try:
            validate_url(rss_url)
        except ValidationError:
            return await ctx.send("The URL provided is not valid!")

        # Check if there is already a RSS/Atom feed with this URL for this channel
        if RssFeeds.objects.filter(
            url__iexact=rss_url, discord_channel_id__exact=channel_id
        ).exists():
            return await ctx.send(
                "A RSS/Atom feed with this URL already exists for this channel"
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

        return await ctx.send(f'RSS/Atom feed "{rss_name}" added to this channel')

    @commands.command(pass_context=True)
    @sender_is_admin()
    async def rss_list(self, ctx):
        """
        List all RSS/Atom feeds for the current Discord channel
        """

        await ctx.trigger_typing()

        channel_id = ctx.message.channel.id
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

        return await ctx.send(payload)

    @commands.command(pass_context=True)
    @sender_is_admin()
    async def rss_delete(self, ctx, rss_feed_id: int):
        """
        Remove a RSS/Atom feed from the current Discord channel
        """

        await ctx.trigger_typing()

        channel_id = ctx.message.channel.id

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

        return await ctx.send(payload)

    @rss_delete.error
    async def rss_delete_error(self, ctx, error):
        if isinstance(
            error, discord.ext.commands.errors.MissingRequiredArgument
        ) or isinstance(error, discord.ext.commands.CommandInvokeError):
            await ctx.send(
                "You didn't provide a numeric value for the RSS/Atom ID you want to "
                "remove.\n\nExample:\n```!rss_delete 5```To remove RSS/Atom feed "
                "wth the ID 5.\nYou find a list of RSS/Atom feeds for this channel "
                "with `!rss_list`"
            )

    @commands.command(pass_context=True)
    @sender_is_admin()
    async def rss_enable(self, ctx, rss_feed_id: int):
        """
        Enable a disabled RSS/Atom feed for the current Discord channel
        """

        await ctx.trigger_typing()

        channel_id = ctx.message.channel.id

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

        return await ctx.send(payload)

    @rss_enable.error
    async def rss_enable_error(self, ctx, error):
        if isinstance(
            error, discord.ext.commands.errors.MissingRequiredArgument
        ) or isinstance(error, discord.ext.commands.CommandInvokeError):
            await ctx.send(
                "You didn't provide a numeric value for the RSS/Atom ID you want to "
                "enable.\n\nExample:\n```!rss_enable 5```To enable RSS/Atom feed wth "
                "the ID 5.\nYou find a list of RSS/Atom feeds for this channel "
                "with `!rss_list`"
            )

    @commands.command(pass_context=True)
    @sender_is_admin()
    async def rss_disable(self, ctx, rss_feed_id: int):
        """
        Disable an enabled RSS/Atom feed for the current Discord channel
        """

        await ctx.trigger_typing()

        channel_id = ctx.message.channel.id

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

        return await ctx.send(payload)

    @rss_disable.error
    async def rss_disable_error(self, ctx, error):
        if isinstance(
            error, discord.ext.commands.errors.MissingRequiredArgument
        ) or isinstance(error, discord.ext.commands.CommandInvokeError):
            await ctx.send(
                "You didn't provide a numeric value for the RSS/Atom ID you want to "
                "enable.\n\nExample:\n```!rss_disable 5```To disable RSS/Atom feed "
                "wth the ID 5.\nYou find a list of RSS/Atom feeds for this channel "
                "with `!rss_list`"
            )


def setup(bot):
    """
    setup the cog
    :param bot:
    """

    bot.add_cog(Rss(bot))
