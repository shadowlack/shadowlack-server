from django.db import models


class CharRosterManager(models.Manager):
    @property
    def active(self):
        """Gets our Active roster"""
        return self.get_or_create(name="Active")[0]
