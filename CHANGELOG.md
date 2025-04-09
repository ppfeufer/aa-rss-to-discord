# Change Log

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).

<!--
GitHub MD Syntax:
https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax

Highlighting:
https://docs.github.com/assets/cb-41128/mw-1440/images/help/writing/alerts-rendered.webp

> [!NOTE]
> Highlights information that users should take into account, even when skimming.

> [!IMPORTANT]
> Crucial information necessary for users to succeed.

> [!WARNING]
> Critical content demanding immediate user attention due to potential risks.
-->

## [In Development] - Unreleased

<!--
Section Order:

### Added
### Fixed
### Changed
### Deprecated
### Removed
### Security
-->

### Added

- Type hinting for managers

## [2.3.0] - 2025-04-07

### Added

- Python 3.13 to the test matrix

### Changed

- Switch to slash commands for the Discord bot commands (See [Discord Bot Commands](https://github.com/ppfeufer/aa-rss-to-discord#discord-bot-commands))
- Set user agent according to MDN guidelines

## [2.2.0] - 2024-09-16

### Changed

- Dependencies updated
  - `allianceauth`>=4.3.1
- French translation improved
- Japanese translation improved
- Lingua codes updated to match Alliance Auth v4.3.1

## [2.1.0] - 2024-07-30

### Changed

- French translation updated

### Removed

- Support for Python 3.8 and Python 3.9

## [2.0.1] - 2024-05-16

### Changed

- Translations updated

## [2.0.0] - 2024-03-16

> [!NOTE]
>
> **This version needs at least Alliance Auth v4.0.0!**
>
> Please make sure to update your Alliance Auth instance **before**
> you install this version, otherwise, an update to Alliance Auth will
> be pulled in unsupervised.

### Added

- Compatibility to Alliance Auth v4
  - Bootstrap 5
  - Django 4.2

### Changed

- App title is now translatable
- Templates changed to Bootstrap 5

### Removed

- Compatibility to Alliance Auth v3

## [2.0.0-beta.2] - 2024-02-19

> [!NOTE]
>
> **This version needs at least Alliance Auth v4.0.0b1!**
>
> Please make sure to update your Alliance Auth instance **before**
> you install this version, otherwise, an update to Alliance Auth will
> be pulled in unsupervised.

### Fixed

- Project classifier in `pyproject.toml`

## [2.0.0-beta.1] - 2024-02-18

> [!NOTE]
>
> **This version needs at least Alliance Auth v4.0.0b1!**
>
> Please make sure to update your Alliance Auth instance **before**
> you install this version, otherwise, an update to Alliance Auth will
> be pulled in unsupervised.

### Added

- Compatibility to Alliance Auth v4
  - Bootstrap 5
  - Django 4.2

### Changed

- App title is now translatable
- Templates changed to Bootstrap 5

### Removed

- Compatibility to Alliance Auth v3

## [1.8.2] - 2023-10-30

> [!NOTE]
>
> **This is the last version compatible with Alliance Auth v3.**

### Changed

- Switching away from deprecated discordbot API

## [1.8.1] - 2023-09-26

### Changed

- Translations updated
- Test suite updated

## [1.8.0] - 2023-08-29

### Added

- Korean translation

## [1.7.0] - 2023-08-15

### Added

- Spanish translation
- Ukrainian translation

## [1.6.0] - 2023-04-25

### Changed

- Moved the build process to PEP 621 / pyproject.toml

## [1.5.0] - 2023-04-16

### Added

- Russian translation

## [1.4.2] - 2023-04-13

### Added

- German translation

## [1.4.1] - 2023-01-15

### Added

- More Debug logging for the task to figure out what's going on for issue #23

### Changed

- Requirements:
  - Alliance Auth >= 3.0.0
- Switched to Allianceauth App Utils for better logging

## [1.4.0] - 2022-05-09

### Added

- Test suite for AA 3.x and Django 4

## Changed

- Switched to `setup.cfg` as config file, since `setup.py` is deprecated now
- Requirements:
  - Alliance Auth >= 2.11.0
  - Allianceauth Discordbot >= 3.0.5

### Removed

- Deprecated settings
- Support for Python 3.7, since `allianceauth-discordbot` needs at least Python 3.8

## [1.3.1] - 2022-02-04

### Added

- Tests for Python 3.11

### Changed

- Requirements:
  - Alliance Auth >= 2.9.4
  - Allianceauth Discordbot < 3.0.0 (Until this bug is fixed » https://github.com/pvyParts/allianceauth-discordbot/issues/56)

## [1.3.0] - 2021-11-30

### Changed

- Minimum requirements
  - Python 3.7
  - Alliance Auth v2.9.3

## [1.2.1] - 2021-11-17

### Fixed

- Min python version is 3.7

## [1.2.0] - 2021-11-16

### Added

- Basic test suite

### Changed

- Minimum requirements

## [1.1.2] - 2021-10-19

### Changed

- Task improved so it doesn't throw a confusing log message

## [1.1.1] - 2021-09-03

### Changed

- Added some sanity checks to the task

## [1.1.0] - 2021-09-03

### Added

- Commands for the Discord bot to manage RSS/Atom feeds. The following commands have
  been added:

  | Command                         | Options                                                                               | What it does                                                     |
  | :------------------------------ | :------------------------------------------------------------------------------------ | :--------------------------------------------------------------- |
  | `!rss_add <rss_url> <rss_name>` | `rss_url` - The URL of the RSS/Atom feed<br>`rss_name` - A Name for the RSS/Atom Feed | Adding a RSS/Atom feed to the current channel                    |
  | `!rss_delete <rss_feed_id>`     | `rss_feed_id` - The ID of the RSS/Atom feed you want to remove                        | Remove a RSS/Atom feed from the current Discord channel          |
  | `!rss_disable <rss_feed_id>`    | `rss_feed_id` - The ID of the RSS/Atom feed you want to disable                       | Disable an enabled RSS/Atom feed for the current Discord channel |
  | `!rss_enable <rss_feed_id>`     | `rss_feed_id` - The ID of the RSS/Atom feed you want to enable                        | Enable a disabled RSS/Atom feed for the current Discord channel  |
  | `!rss_list`                     | None                                                                                  | List all RSS/Atom feeds for the <br/>current Discord channel     |

## [1.0.0] - 2021-09-03

### Changed

- Moved from Beta to Stable

## [0.1.0-beta.7] - 2021-07-08

### Added

- Tested for compatibility with Python 3.9 and Django 3.2

## [0.1.0-beta.6] - 2021-05-27

### Changed

- Update the last item instead of removing and adding it again

## [0.1.0-beta.5] - 2021-05-25

### Added

- Switch to enable/disable RSS feeds in admin interface

### Changed

- Cleaned up the filter in admin interface

## [0.1.0-beta.4] - 2021-05-05

### Fixed

- Using Django application registry instead of directly accessing `INSTALLED_APPS`

## [0.1.0-beta.3] - 2021-04-30

### Fixed

- SQL error when there are emojis in the RSS title

## [0.1.0-beta.2] - 2021-04-30

### Changed

- Last item check via db instead of redis cache

### ⚠️ Important ⚠️

Migrations have been reset. Run **before** updating via pip:

```shell
python myauth/manage.py migrate aa_rss_to_discord zero
```

Run migrations after updating as usual.

## [0.1.0-beta.1] - 2021-04-29

- First public beta release
