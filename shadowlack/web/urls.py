"""
Url definition file to redistribute incoming URL requests to django
views. Search the Django documentation for "URL dispatcher" for more
help.

"""
from django.urls import path, include

# default evennia patterns
from evennia.web.urls import urlpatterns
import paxboards.urls

from web.codex.views import contact_form

# eventual custom patterns
custom_patterns = [
    path("contact/", contact_form, name="contact"),

    # url(r'/desired/url/', view, name='example'),
    path("", include("web.character.urls")),
    path("codex/", include("web.codex.urls")),
    path("forums/", include("paxboards.urls", namespace='board'))
]

# this is required by Django.
urlpatterns = custom_patterns + urlpatterns
