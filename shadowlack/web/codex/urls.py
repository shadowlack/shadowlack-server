from django.conf.urls import url
from django.urls import path, include

from evennia.web.website import views as website_views

from web.codex.views import codex_list

urlpatterns = [
    url(
        r"^(?P<category>[\w\d\-]+)/(?P<topic>[\w\d\-]+)/$",
        website_views.HelpDetailView.as_view(),
        name="entry",
    ),
    path("", codex_list, name="codex"),
]
