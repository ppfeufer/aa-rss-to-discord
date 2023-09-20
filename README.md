# Alliance Auth RSS to Discord<a name="alliance-auth-rss-to-discord"></a>

[![Version](https://img.shields.io/pypi/v/aa-rss-to-discord?label=release)](https://pypi.org/project/aa-rss-to-discord/)
[![License](https://img.shields.io/github/license/ppfeufer/aa-rss-to-discord)](https://github.com/ppfeufer/aa-rss-to-discord/blob/master/LICENSE)
[![Python](https://img.shields.io/pypi/pyversions/aa-rss-to-discord)](https://pypi.org/project/aa-rss-to-discord/)
[![Django](https://img.shields.io/pypi/djversions/aa-rss-to-discord?label=django)](https://pypi.org/project/aa-rss-to-discord/)
![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/ppfeufer/aa-rss-to-discord/master.svg)](https://results.pre-commit.ci/latest/github/ppfeufer/aa-rss-to-discord/master)
[![Code Style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](http://black.readthedocs.io/en/latest/)
[![Discord](https://img.shields.io/discord/790364535294132234?label=discord)](https://discord.gg/zmh52wnfvM)
[![Checks](https://github.com/ppfeufer/aa-rss-to-discord/actions/workflows/automated-checks.yml/badge.svg)](https://github.com/ppfeufer/aa-rss-to-discord/actions/workflows/automated-checks.yml)
[![codecov](https://codecov.io/gh/ppfeufer/aa-rss-to-discord/branch/master/graph/badge.svg?token=LVEQ6W55ZB)](https://codecov.io/gh/ppfeufer/aa-rss-to-discord)
[![Badge: Translation Status]][weblate engage]
[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-2.1-4baaaa.svg)](https://github.com/ppfeufer/aa-rss-to-discord/blob/master/CODE_OF_CONDUCT.md)

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/N4N8CL1BY)

A simple app to post selected RSS feeds to your Discord.

______________________________________________________________________

<!-- mdformat-toc start --slug=github --maxlevel=6 --minlevel=1 -->

- [Alliance Auth RSS to Discord](#alliance-auth-rss-to-discord)
  - [Installation](#installation)
    - [Step 0.5: Install AA-Discordbot](#step-05-install-aa-discordbot)
    - [Step 1: Install the Package](#step-1-install-the-package)
    - [Step 2: Configure Alliance Auth](#step-2-configure-alliance-auth)
    - [Step 3: Finalizing the Installation](#step-3-finalizing-the-installation)
    - [Step 4: Configure your RSS Feeds](#step-4-configure-your-rss-feeds)
  - [Discord Bot Commands](#discord-bot-commands)
  - [Updating](#updating)
  - [Changelog](#changelog)
  - [Translation Status](#translation-status)
  - [Contributing](#contributing)

<!-- mdformat-toc end -->

______________________________________________________________________

## Installation<a name="installation"></a>

**Important**: Please make sure you meet all preconditions before you proceed:

- Alliance Auth RSS to Discord is a plugin for Alliance Auth. If you don't have Alliance Auth running
  already, please install it first before proceeding. (see the official
  [AA installation guide](https://allianceauth.readthedocs.io/en/latest/installation/allianceauth.html) for details)
- Alliance Auth RSS to Discord needs [AA-Discordbot](https://github.com/pvyParts/allianceauth-discordbot)
  to interact with your Discord server. Make sure it is installed and configured
  **before** installing this app.

### Step 0.5: Install AA-Discordbot<a name="step-05-install-aa-discordbot"></a>

In order for this app to work, you need to install and configure
[AA-Discordbot](https://github.com/pvyParts/allianceauth-discordbot) first. Read the
instructions how to do so in the README of AA-Discordbot.

### Step 1: Install the Package<a name="step-1-install-the-package"></a>

Make sure you're in the virtual environment (venv) of your Alliance Auth
installation Then install the latest release directly from PyPi.

```shell
pip install aa-rss-to-discord
```

### Step 2: Configure Alliance Auth<a name="step-2-configure-alliance-auth"></a>

This is fairly simple, just add the following to the `INSTALLED_APPS` of your `local.py`

Configure your AA settings (`local.py`) as follows:

- Add `"aa_rss_to_discord",` to `INSTALLED_APPS`
- Add the scheduled task
  ```python
  CELERYBEAT_SCHEDULE["aa_rss_to_discord_fetch_rss"] = {
      "task": "aa_rss_to_discord.tasks.fetch_rss",
      "schedule": crontab(minute="*/5"),
  }
  ```

### Step 3: Finalizing the Installation<a name="step-3-finalizing-the-installation"></a>

Run migrations to finalize the installation

```shell
python manage.py migrate
```

Finally, restart your supervisor services for AA.

### Step 4: Configure your RSS Feeds<a name="step-4-configure-your-rss-feeds"></a>

First, you need to set up the Discord Server and Channels. For this, you go in your
admin backend to the Discordbot settings and enter the needed information there.

When done, you can set up your RSS feeds. This can be done in the setting of this
app, still in your admin backend. Create a new RSS Feed entry, enter the name, url
and select the Discord channel it should be posted to. Once done, save it.

## Discord Bot Commands<a name="discord-bot-commands"></a>

The following commands are available for the Discord bot to manage RSS/Atom feeds:

| Command                         | Options                                                                                   | What it does                                                     |
| :------------------------------ | :---------------------------------------------------------------------------------------- | :--------------------------------------------------------------- |
| `!rss_add <rss_url> <rss_name>` | - `rss_url` - The URL of the RSS/Atom feed<br>- `rss_name` - A Name for the RSS/Atom Feed | Adding a RSS/Atom feed to the current channel                    |
| `!rss_delete <rss_feed_id>`     | `rss_feed_id` - The ID of the RSS/Atom feed you want to remove                            | Remove a RSS/Atom feed from the current Discord channel          |
| `!rss_disable <rss_feed_id>`    | `rss_feed_id` - The ID of the RSS/Atom feed you want to disable                           | Disable an enabled RSS/Atom feed for the current Discord channel |
| `!rss_enable <rss_feed_id>`     | `rss_feed_id` - The ID of the RSS/Atom feed you want to enable                            | Enable a disabled RSS/Atom feed for the current Discord channel  |
| `!rss_list`                     | None                                                                                      | List all RSS/Atom feeds for the current Discord channel          |

## Updating<a name="updating"></a>

To update your existing installation of Alliance Auth RSS to Discord, first enable your
virtual environment (venv) of your Alliance Auth installation.

```bash
pip install -U aa-rss-to-discord

python manage.py migrate
```

Finally, restart your supervisor services for AA.

## Changelog<a name="changelog"></a>

See [CHANGELOG.md]

## Translation Status<a name="translation-status"></a>

[![Translation status](https://weblate.ppfeufer.de/widget/alliance-auth-apps/aa-rss-to-discord/multi-auto.svg)](https://weblate.ppfeufer.de/engage/alliance-auth-apps/)

Do you want to help translate this app into your language or improve the existing
translation? - [Join our team of translators][weblate engage]!

## Contributing<a name="contributing"></a>

Do you want to contribute to this project? That's cool!

Please make sure to read the [Contribution Guidelines].\
(I promise, it's not much, just some basics)

<!-- Links -->

[badge: translation status]: https://weblate.ppfeufer.de/widget/alliance-auth-apps/aa-rss-to-discord/svg-badge.svg "Translation Status"
[changelog.md]: https://github.com/ppfeufer/aa-rss-to-discord/blob/master/CHANGELOG.md "Changelog"
[contribution guidelines]: https://github.com/ppfeufer/aa-rss-to-discord/blob/master/CONTRIBUTING.md "Contribution Guidelines"
[weblate engage]: https://weblate.ppfeufer.de/engage/alliance-auth-apps/ "Weblate Translations"
