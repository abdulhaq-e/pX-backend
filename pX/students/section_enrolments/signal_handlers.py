# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from .models import SectionEnrolment
from ...administration.courses.assessments.models import Assessment


def on_save_section_enrolment(sender, instance, **kwargs):
    '''
    All saved enrolments should have assessment_results,
    upon creating the section enrolment, the assessment_results
    should be created and linked to their section_enrolment

    Prior to that, the assessments themselves need to be ready,
    this is done elsewhere (after creating the period courses)
    '''

    if sender != SectionEnrolment:
        return

    for assessment in Assessment.objects.filter(
            period_course=instance.section.period_course):
        instance.assessment_results.get_or_create(
            assessment=assessment)
