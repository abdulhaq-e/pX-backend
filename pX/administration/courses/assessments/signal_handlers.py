# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import apps

from .models import (AssessmentType, Assessment, AssessmentResult)

from django.contrib.contenttypes.models import ContentType

from ....notifications.models import Notification


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


# i won't use signals for emails yet
# def on_save_assessment_result(sender, instance, **kwargs):

#     if sender != AssessmentResult:
#         return

#     notifications = Notification.objects.filter(
#         content_type=ContentType.objects.get_for_model(instance),
#         object_id=instance.pk)

#     if not notifications.exists():  # and notifications.last():
#         print("hit")
