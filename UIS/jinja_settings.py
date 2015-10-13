from django.contrib.staticfiles.storage import staticfiles_storage
from django.core.urlresolvers import reverse

from jinja2 import Environment


def environment(**options):

    options.pop('autoescape')
    env = Environment(autoescape=False, **options)
    env.globals.update({
        'static': staticfiles_storage.url,
        'url': reverse,
    })
    return env
