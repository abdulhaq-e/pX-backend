# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from modeltranslation.translator import register, TranslationOptions

from .models import Administration, Faculty, Department


@register(Administration)
class AdministrationTranslationOptions(TranslationOptions):

    fields = ('name',)


@register(Faculty)
class FacultyTranslationOptions(TranslationOptions):

    fields = tuple()


@register(Department)
class DepartmentTranslationOptions(TranslationOptions):

    fields = ('acronym', )
