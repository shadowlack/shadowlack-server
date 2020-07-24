# Shadowlack
[![license: CC BY-NC-SA 4.0](https://img.shields.io/badge/license-CC%20BY--NC--SA%204.0-lightgrey.svg)]() [![evennia](https://img.shields.io/badge/evennia-0.9--beta-%23E7672E)](http://www.evennia.com/) [![Join us on Discord](https://img.shields.io/discord/140589809231069184?logo=discord)](https://discord.gg/BNhwAm9) ![](https://img.shields.io/badge/kill-grue-purple.svg)

This repository contains data that is specific to the Shadowlack roleplaying game.

It is under a CC BY-NC-SA 4.0 license as it contains some player writing and media that may not be used outside of Shadowlack's game context without attribution.

## Requirements

* [Python](http://www.python.org/) 3.8
  * [virtualenv](http://pypi.python.org/pypi/virtualenv) for making an isolated Python environment. `pip install virtualenv`
* [A database](https://github.com/evennia/evennia/wiki/Choosing-An-SQL-Server). SQLite3, MariaDB, or PostgreSQL, will work.

## Installation

1. `git clone --recurse-submodules https://github.com/shriker/shadowlack-server.git`
1. `cd shadowlack-server`
1. `virtualenv evenv`

    Your working directory structure should look like this:
    ```
    shadowlack-server/
        evennia/
        evenv/
        shadowlack/
    ```
1. `source evenv/bin/activate` (Linux, Mac), or `evenv\Scripts\activate` (Windows, PS Shell, Git Bash)
1. `pip install -e evennia`
1. `pip install -r requirements.txt`
1. `cd shadowlack`
1. Copy `shadowlack/server/conf/.env.example` to `shadowlack/server/conf/.env` and edit your database variables.
1. `evennia migrate`
1. `evennia start`

### Server Commands

Must be run within the `shadowlack` directory.

```bash
evennia start
evennia reload
evennia stop
```

## Development

Running `evennia start` for the first time will prompt you to create a new super user account.

### Migrations

```bash
evennia makemigrations
evennia migrate
```

### Testing

```bash
evennia --settings settings.py test commands
evennia test --settings settings.py
```

### Content Seeding

As a super user, run the following commands in the Web Client to seed content. This will seed both the Codex, as well as content flat pages.

```bash
batchcode seeder_codex
batchcode seeder_pages
```

## Links 🔗

* [Shadowlack](https://shadowlack.com)
* [Evennia Documentation](http://www.evennia.com/)
