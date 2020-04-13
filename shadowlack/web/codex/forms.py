from django import forms


class ContactForm(forms.Form):
    subject = forms.CharField(required=True, max_length=100)
    sender = forms.EmailField(required=True, label='Your Email')
    message = forms.CharField(widget=forms.Textarea, required=True)
