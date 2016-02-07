# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from modeltranslation.translator import register, TranslationOptions

from .models import AssessmentType


@register(AssessmentType)
class PersonTranslationOptions(TranslationOptions):

    fields = ('assessment_type', )
