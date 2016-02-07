# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig


class SectionEnrolmentAppConfig(AppConfig):

    name = "pX.students.section_enrolments"
    label = "section_enrolments"
    verbose_name = "Section Enrolments"

    def ready(self):
        from . import signals
        signals.connect_section_enrolment_signals()
