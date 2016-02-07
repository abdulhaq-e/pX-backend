# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from modeltranslation.translator import register, TranslationOptions

from .models import Student


@register(Student)
class StudentTranslationOptions(TranslationOptions):
    pass
    # fields = ('first_name', 'last_name',)
