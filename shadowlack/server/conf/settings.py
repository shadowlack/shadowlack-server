# Use the defaults from Evennia unless explicitly overridden
from evennia.settings_default import *

SERVERNAME = "Shadowlack"
GAME_SLOGAN = "Original Science Fantasy World Building"

GAME_INDEX_ENABLED = False
GAME_INDEX_LISTING = {
    "game_name": SERVERNAME,
    "game_status": "pre-alpha",  # pre-alpha, alpha, beta or launched
    "short_description": GAME_SLOGAN,
    "long_description": "Shadowlack is a free multi-user text adventure, play-by-post game, and an ongoing world-building project. Based on the Fate Core System.",
    "listing_contact": "graders@shadowlack.com",  # email
    "telnet_hostname": "",  # mygame.com
    "telnet_port": "",  # 1234
    "game_website": "https://shadowlack.com",  # http://mygame.com
    "web_client_url": "",  # http://mygame.com/webclient
}

INSTALLED_APPS += (
    'compressor',
    'paxboards',
    'web.character',
    'web.codex',
    'web.mudbuild',
)

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
]

COMPRESS_PRECOMPILERS = (
    ('text/x-scss', 'django_libsass.SassCompiler'),
    ('text/x-sass', 'django_libsass.SassCompiler'),
)

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

MULTISESSION_MODE = 2
MAX_NR_CHARACTERS = 4

TELNET_ENABLED = False
TELNET_PORTS = [4000]
TELNET_INTERFACES = ["0.0.0.0"]
TELNET_OOB_ENABLED = False

# Activate Telnet+SSL protocol (SecureSocketLibrary) for supporting clients
SSL_ENABLED = False
SSL_PORTS = [8802]
SSL_INTERFACES = ["0.0.0.0"]
SSH_ENABLED = False
SSH_PORTS = [8022]
SSH_INTERFACES = ["0.0.0.0"]

# The default home location used for all objects. This is used as a
# fallback if an object's normal home location is deleted. Default
# is Limbo (#2).
DEFAULT_HOME = "#2"
# The start position for new characters. Default is Limbo (#2).
#  MULTISESSION_MODE = 0, 1 - used by default unloggedin create command
#  MULTISESSION_MODE = 2, 3 - used by default character_create command
START_LOCATION = "#2"

# Game Time setup
TIME_FACTOR = 4
TIME_GAME_EPOCH = 0
TIME_UNITS = {
    "sec": 1,
    "min": 60,
    "hour": 60 * 60,
    "day": 60 * 60 * 24,
    "month": 60 * 60 * 24 * 30,
    "year": 60 * 60 * 24 * 30 * 12,
}
TIME_IGNORE_DOWNTIMES = True

SITE_ID = 2
EVENNIA_ADMIN = False

COMMAND_DEFAULT_CLASS = "commands.command.MuxCommand"

# colours
# Extend the available regexes for adding XTERM256 colors in-game. This is given
# as a list of regexes, where each regex must contain three anonymous groups for
# holding integers 0-5 for the red, green and blue components Default is
# is r'\|([0-5])([0-5])([0-5])', which allows e.g. |500 for red.
# XTERM256 foreground color replacement
COLOR_XTERM256_EXTRA_FG = [
    r'\|([0-5])([0-5])([0-5])',
    r'\|([0-2])([0-9])([0-9])',
]

DEBUG = True
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.BCryptPasswordHasher',
    'django.contrib.auth.hashers.SHA1PasswordHasher',
    'django.contrib.auth.hashers.MD5PasswordHasher',
    'django.contrib.auth.hashers.UnsaltedSHA1PasswordHasher',
    'django.contrib.auth.hashers.UnsaltedMD5PasswordHasher',
    'django.contrib.auth.hashers.CryptPasswordHasher',
]

######################################################################
# Settings given in secret_settings.py override those in this file.
######################################################################
try:
    from server.conf.secret_settings import *
except ImportError:
    print("secret_settings.py file not found or failed to import.")
