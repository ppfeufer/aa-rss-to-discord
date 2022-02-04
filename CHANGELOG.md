# Change Log

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/)


## [In Development] - Unreleased


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

  | Command | Options | What it does |
  |:---|:---|:---|
  | `!rss_add <rss_url> <rss_name>` | - `rss_url` - The URL of the RSS/Atom feed<br>- `rss_name` - A Name for the RSS/Atom Feed | Adding a RSS/Atom fedd to the current channel |
  | `!rss_delete <rss_feed_id>` | `rss_feed_id` - The ID of the RSS/Atom feed you want to remove |  Remove a RSS/Atom feed from the current Discord channel |
  | `!rss_disable <rss_feed_id>` | `rss_feed_id` - The ID of the RSS/Atom feed you want to disable |  Disable an enabled RSS/Atom feed for the current Discord channel |
  | `!rss_enable <rss_feed_id>` | `rss_feed_id` - The ID of the RSS/Atom feed you want to enable |  Enable a disabled RSS/Atom feed for the current Discord channel |
  | `!rss_list` | None |  List all RSS/Atom feeds for the current Discord channel |


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

- Cleaned up filter in admin interface


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
