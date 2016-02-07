# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from .models import SectionEnrolment
from ...administration.courses.assessments.models import Assessment


def on_save_section_enrolment(sender, instance, **kwargs):

    if sender != SectionEnrolment:
        return

    for assessment in Assessment.objects.filter(
            period_course=instance.section.period_course):
        instance.assessment_results.get_or_create(assessment=assessment)
