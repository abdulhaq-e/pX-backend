# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import apps

from .models import (AssessmentType, Assessment, AssessmentResult)
from .validators import AssessmentGradeValidator

# from django.contrib.contenttypes.models import ContentType

# from ....notifications.models import Notification


def on_migrate_assessment_type(sender, **kwargs):

    if sender != apps.get_app_config("assessments"):
        return

    AssessmentType.objects.get_or_create(assessment_type='Course Work')
    AssessmentType.objects.get_or_create(assessment_type='Final Examination')
    AssessmentType.objects.get_or_create(assessment_type='Total')


def on_save_assessment(sender, instance, **kwargs):

    if sender != Assessment:
        return

    # print(instance.result_status)
    for assessment_result in instance.assessment_results.all():
        # print(result.model)
        assessment_result.save()


def pre_save_assessment_result(sender, instance, **kwargs):

    if sender != AssessmentResult:
        return

    instance.grade = None

    if instance._grade is None:
        return
    else:
        AssessmentGradeValidator(instance._grade,
                                 instance.assessment.total_grade)()
        if not instance.hidden and instance.assessment.result_status == 'P':
            instance.grade = instance._grade

    section_enrolment = instance.section_enrolment
    section_enrolment.grade = instance.grade
    section_enrolment.save()


# i won't use signals for emails yet
# def on_save_assessment_result(sender, instance, **kwargs):

#     if sender != AssessmentResult:
#         return

#     notifications = Notification.objects.filter(
#         content_type=ContentType.objects.get_for_model(instance),
#         object_id=instance.pk)

#     if not notifications.exists():  # and notifications.last():
#         print("hit")
