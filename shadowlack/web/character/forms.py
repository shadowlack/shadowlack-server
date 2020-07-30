from django import forms
from evennia.web.website.forms import CharacterForm

from typeclasses import characters
from world import species, skills

# species.ALL_SPECIES

class ShadowlackCharacterForm(CharacterForm):
    """
    https://docs.djangoproject.com/en/3.0/ref/forms/widgets/
    """
    sdesc = forms.CharField(
        label="Short Description",
        max_length=2048,
        required=False,
        widget=forms.Textarea(attrs={"rows": 1}),
        help_text="A short description of your character.",
    )
    age = forms.IntegerField(
        label="Age",
        min_value=18, max_value=9000,
        help_text="How old is your character.")
