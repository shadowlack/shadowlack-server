# shadowlack/world/seeder_pages.py
# run as super user:
# batchcode seeder_pages

# HEADER

from pathlib import Path
from django.contrib.sites.models import Site
from django.contrib.flatpages.models import FlatPage

# CODE

# List of pages to process
pages = [
    ['/about/', 'page_about.html', 'About'],
    ['/anti-harassment-policy/', 'page_harassment.html', 'Anti-Harassment Policy'],
    ['/legal/', 'page_legal.html', 'Terms and Conditions'],
    ['/licensing/', 'page_licensing.html', 'Licensing'],
    ['/parents/', 'page_parents.html', 'For Parents'],
    ['/privacy/', 'page_privacy.html', 'Privacy Policy'],
    ['/rules/', 'page_rules.html', 'Rules and Regulations'],
    ['/staff-handbook/', 'page_staff.html', 'Staff Handbook'],
]

# Loop through and create or update the pages
for page in pages:

    page_content = Path("world/flatpages/" + page[1]).read_text()
    obj, created = FlatPage.objects.update_or_create(url=page[0])

    obj.title = page[2]
    obj.content = page_content
    obj.save()

    if created:
        # Add page to a site if it's being created
        obj.sites.add(Site.objects.all()[0])
        obj.save()
        caller.msg("{} page created.".format(page[0]))
    else:
        caller.msg("{} page updated.".format(page[0]))
