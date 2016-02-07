# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig


class AssessmentsAppConfig(AppConfig):

    name = "pX.administration.courses.assessments"
    label = "assessments"
    verbose_name = "Assessments"

    def ready(self):
        from . import signals
        signals.connect_assessment_type_signals()
        signals.connect_assessment_signals()
        # signals.connect_assessment_result_signals()
