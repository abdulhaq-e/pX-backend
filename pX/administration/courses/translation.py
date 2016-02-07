# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from modeltranslation.translator import register, TranslationOptions

from .models import Course, SubSectionType, Section


@register(Course)
class CourseTranslationOptions(TranslationOptions):

    fields = ('name', 'course_description', 'course_syllabus')


@register(SubSectionType)
class SectionTypeTranslationOptions(TranslationOptions):

    fields = ('name', )


@register(Section)
class SectionTranslationOptions(TranslationOptions):

    fields = ('name', )
