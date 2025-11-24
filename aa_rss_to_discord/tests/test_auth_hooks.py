# Standard Library
from unittest import mock

# AA RSS to Discord
from aa_rss_to_discord.auth_hooks import register_cogs
from aa_rss_to_discord.tests import BaseTestCase


class TestAuthHooks(BaseTestCase):
    """
    Test the auth hooks
    """

    def test_registers_discord_cogs_hook_correctly(self):
        """
        Tests that the discord cogs hook is registered correctly.

        :return:
        :rtype:
        """

        result = register_cogs()

        self.assertIn("aa_rss_to_discord.discordbot.cogs.rss", result)

    def test_returns_list_of_cogs(self):
        """
        Tests that the register_cogs function returns a list.

        :return:
        :rtype:
        """

        result = register_cogs()

        self.assertIsInstance(result, list)

    def test_handles_empty_hook_registration_gracefully(self):
        """
        Tests that the register_cogs function handles an empty hook registration gracefully.

        :return:
        :rtype:
        """

        with mock.patch("allianceauth.hooks.register", return_value=None):
            result = register_cogs()

            self.assertIsNotNone(result)
