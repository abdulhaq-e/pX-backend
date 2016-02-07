# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db.models import Q

from .models import PeriodCourse
from .assessments.models import AssessmentType


def on_save_period_course(sender, instance, **kwargs):

    if sender != PeriodCourse:
        return

    try:
        course_work = AssessmentType.objects.get(assessment_type='Course Work')
        if not instance.assessments.filter(
                assessment_type__assessment_type='Course Work').exists():
            instance.assessments.create(assessment_type=course_work,
                                        total_grade=40)
    except AssessmentType.DoesNotExist:
        pass

    try:
        final_exam = AssessmentType.objects.get(
            assessment_type='Final Examination')
        if not instance.assessments.filter(
                assessment_type__assessment_type='Final Examination').exists():
            instance.assessments.create(assessment_type=final_exam,
                                        total_grade=60)
    except AssessmentType.DoesNotExist:
        pass

    try:
        total = AssessmentType.objects.get(assessment_type='Total')
        if not instance.assessments.filter(
                assessment_type__assessment_type='Total').exists():
            instance.assessments.create(assessment_type=total,
                                        total_grade=100)
    except AssessmentType.DoesNotExist:
        pass
