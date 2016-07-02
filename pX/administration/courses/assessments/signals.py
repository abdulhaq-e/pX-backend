# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db.models import signals
from django.apps import apps

from . import signal_handlers


def connect_assessment_type_signals():

    signals.post_migrate.connect(signal_handlers.on_migrate_assessment_type,
                                 sender=apps.get_app_config("assessments"),
                                 dispatch_uid="assessment_type_migrated")


def disconnect_assessment_type_signals():

    signals.post_save.disconnect(sender=apps.get_app_config("assessments"),
                                 dispatch_uid="assessment_type_migrated")


def connect_assessment_signals():

    signals.post_save.connect(signal_handlers.on_save_assessment,
                              sender=apps.get_model("assessments.Assessment"),
                              dispatch_uid="assessment_saved")


def disconnect_asessement_signals():

    signals.post_save.disconnect(sender=apps.get_model("assessments.Assessment"),
                                 dispatch_uid="assessment_saved")


def connect_assessment_result_signals():

    signals.pre_save.connect(signal_handlers.pre_save_assessment_result,
                             sender=apps.get_model("assessments.AssessmentResult"),
                             dispatch_uid="assessment_result_pre_save")


def disconnect_assessment_result_signals():

    signals.pre_save.disconnect(
        sender=apps.get_model("assessments.AssessmentResult"),
        dispatch_uid="assessment_result_pre_save")

# i won't use signals for emails yet
# def connect_assessment_result_signals():

#     signals.post_save.connect(
#         signal_handlers.on_save_assessment_result,
#         sender=apps.get_model("assessments.AssessmentResult"),
#         dispatch_uid="assessment_result_saved")
