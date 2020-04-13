from django.core.exceptions import PermissionDenied
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from django.conf import settings
from django.urls import reverse
from django.utils.text import slugify

from evennia.help.models import HelpEntry

from .forms import ContactForm

def codex_list(request):
    user = request.user

    try:
        all_topics = []
        for topic_ob in HelpEntry.objects.all():
            try:
                if topic_ob.access(user, 'view', default=True):
                    all_topics.append(topic_ob)
            except AttributeError:
                continue
        all_topics = sorted(all_topics, key=lambda entry: entry.key.lower())
        all_categories = list(set([topic_ob.help_category.capitalize() for topic_ob in all_topics
                                   if topic_ob.access(user, "view")]))
        all_categories = sorted(all_categories)
    except IndexError:
        raise Http404("Error in compiling codex list.")

    return render(request, 'codex/codex_list.html', {
        'all_topics': all_topics,
        'all_categories': all_categories})


def codex_entry(request, object_key):
    object_key = object_key.lower()
    topic_ob = get_object_or_404(HelpEntry, db_key__iexact=object_key)
    can_see = False
    try:
        can_see = topic_ob.access(request.user, 'view', default=True)
    except AttributeError:
        pass
    if not can_see:
        raise PermissionDenied
    return render(request, 'codex/codex_detail.html', {'topic': topic_ob, 'page_title': object_key})


def contact_form(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():

            # User data
            subject = form.cleaned_data['subject']
            sender = form.cleaned_data['sender']
            message = form.cleaned_data['message']

            # System data
            recipients = ['graders@shadowlack.com']
            
            try:
                send_mail(subject, message, sender, recipients)
            except BadHeaderError:
                return HttpResponse('Invalid header found. Nice try though.')
            # Change redirect
            return HttpResponseRedirect('/thanks/')
    else:
        form = ContactForm()
    return render(request, "codex/contact_form.html", {'form': form})


def contact_success(request):
    return HttpResponse('Success! Thank you for your message.')
