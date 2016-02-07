# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from modeltranslation.translator import register, TranslationOptions

from .models import Person


@register(Person)
class PersonTranslationOptions(TranslationOptions):

    fields = ('first_name', 'last_name',)
