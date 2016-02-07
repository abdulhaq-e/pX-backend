# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig


class CoursesAppConfig(AppConfig):

    name = "pX.administration.courses"
    label = "courses"
    verbose_name = "Courses"

    def ready(self):
        from . import signals
        signals.connect_period_course_signals()
