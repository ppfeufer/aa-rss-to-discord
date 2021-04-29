# Alliance Auth RSS to Discord

[![Version](https://img.shields.io/pypi/v/aa-rss-to-discord?label=release)](https://pypi.org/project/aa-rss-to-discord/)
[![License](https://img.shields.io/github/license/ppfeufer/aa-rss-to-discord)](https://github.com/ppfeufer/aa-rss-to-discord/blob/master/LICENSE)
[![Python](https://img.shields.io/pypi/pyversions/aa-rss-to-discord)](https://pypi.org/project/aa-rss-to-discord/)
[![Django](https://img.shields.io/pypi/djversions/aa-rss-to-discord?label=django)](https://pypi.org/project/aa-rss-to-discord/)
![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)
[![Code Style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](http://black.readthedocs.io/en/latest/)
[![Discord](https://img.shields.io/discord/790364535294132234?label=discord)](https://discord.gg/zmh52wnfvM)

A simple app to post selected RSS feeds to your Discord.


## Contents

- [Installation](#installation)
  - [Step 0.5 - Install AA-Discordbot](#step-05---install-aa-discordbot)
  - [Step 1 - Install the Package](#step-1---install-the-package)
  - [Step 2 - Configure Alliance Auth](#step-2---configure-alliance-auth)
  - [Step 3 - Finalize the Installation](#step-3---finalize-the-installation)
  - [Step 4 - Configure your RSS Feeds](#step-4---configure-your-rss-feeds)
- [Updating](#updating)


## Installation

**Important**: Please make sure you meet all preconditions before you proceed:

- Alliance Auth RSS to Discord is a plugin for Alliance Auth. If you don't have Alliance Auth running
  already, please install it first before proceeding. (see the official
  [AA installation guide](https://allianceauth.readthedocs.io/en/latest/installation/allianceauth.html) for details)
- Alliance Auth RSS to Discord needs [AA-Discordbot](https://github.com/pvyParts/allianceauth-discordbot)
  to interact with your Discord server. Make sure it is installed and configured
  **before** installing this app.


### Step 0.5 - Install AA-Discordbot

In order for this app to function, you need to install and configure
[AA-Discordbot](https://github.com/pvyParts/allianceauth-discordbot) first. Read the
instructions how to do so in the README of AA-Discordbot.


### Step 1 - Install the Package

Make sure you are in the virtual environment (venv) of your Alliance Auth
installation Then install the latest releast directly from PyPi.

```shell
pip install aa-rss-to-discord
```


### Step 2 - Configure Alliance Auth

This is fairly simple, just add the following to the `INSTALLED_APPS` of your `local.py`

Configure your AA settings (`local.py`) as follows:

- Add `"aa_rss_to_discord",` to `INSTALLED_APPS`
- Add the scheduled task
  ```python
  if "aa_rss_to_discord" in INSTALLED_APPS:
      CELERYBEAT_SCHEDULE["aa_rss_to_discord_fetch_rss"] = {
          "task": "aa_rss_to_discord.tasks.fetch_rss",
          "schedule": crontab(minute="*/5"),
      }
  ```


### Step 3 - Finalize the Installation

Run migrations to finalize the installation

```shell
python manage.py migrate
```

Finally restart your supervisor services for AA.


### Step 4 - Configure your RSS Feeds

First you need to set up the Discord Server and Channels. For this you go in your
admin backend to the Discordbot settings and enter the needed information there.

When done, you can set up your RSS feeds. This can be done in the setting of this
app, still in your admin backend. Create a new RSS Feed entry, enter the name, url
and select the Discord channel it should be posted to. Once done, save it.


## Updating

To update your existing installation of Alliance Auth RSS to Discord, first enable your
virtual environment (venv) of your Alliance Auth installation.

```bash
pip install -U aa-rss-to-discord

python manage.py migrate
```

Finally restart your supervisor services for AA.
