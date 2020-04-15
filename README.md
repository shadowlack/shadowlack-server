# Shadowlack MU*

Shadowlack Python MU* development.

## Installation
```bash
pip install -e evennia
pip install mysqlclient
```

Starting the server for the first time will give you the option to create a super user account.

```bash
# If you are using a standard command prompt, you can use the following:
evenv\scripts\activate.bat

# If you are using a PS Shell, Git Bash, or other, you can use the following:
.\evenv\scripts\activate

cd shadowlack
# Server controls
evennia start
evennia reload
evennia stop
```

## Development
```bash
evennia makemigrations
evennia migrate
```

## Testing
```bash
evennia --settings settings.py test commands
evennia test --settings settings.py
```

## Content Seeding

As a super user, run the following commands in the web client to seed content. This will seed both the Codex, as well as content flat pages.

```bash
batchcode seeder_codex
batchcode seeder_pages
```