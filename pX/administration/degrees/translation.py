# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from modeltranslation.translator import register, TranslationOptions

from .models import Degree


@register(Degree)
class DegreeTranslationOptions(TranslationOptions):

    fields = ('name', )
