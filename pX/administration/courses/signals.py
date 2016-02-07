# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db.models import signals

from . import signal_handlers


def connect_period_course_signals():

    signals.post_save.connect(signal_handlers.on_save_period_course,
                              sender="courses.PeriodCourse",
                              dispatch_uid="period_course_saved")


def disconnect_period_course_signals():
    signals.post_save.disconnect(sender="courses.PeriodCourse",
                                 dispatch_uid="period_course_saved")
