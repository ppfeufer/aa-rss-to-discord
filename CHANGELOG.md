# Change Log

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/)


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
