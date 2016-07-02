# -*- coding: utf-8 -*-
from __future__ import division, unicode_literals

import uuid

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible

from ...base.models import pXBaseModel
from ..section_enrolments.models import SectionEnrolment


@python_2_unicode_compatible
class PeriodRegistration(pXBaseModel):
    """
    this describes the m2m relation between a student and terms

    TODO: maybe the student registration statuses need to be reviewed!

    random thoughts:

    - registered and suspended students are easy to deal with, but what about
      'dropped' students. Certainly they won't say this term we are dropping
      (i.e. we are not going to register nor are we going to suspend studying).
      the solution is: run something like a cron job to add 'dropped' status to
      all students who didn't register/suspend after a period of time!

    - on 3:15 (a.m.), 16/05/15, i moved most things that i thought should
      belong
      to studentregistration to student degree. I think this bests model
      multiple degrees. I don't know why I'm obsessed by multiple degrees.
      it won't happen in the near feature in our ****** universities.

    - on 2:10 (p.m.) 19/05/15, room K106, I just undo the things I did above.
      thinking about multiple degrees is premature!
    """

    student_registration_id = models.UUIDField(primary_key=True,
                                               default=uuid.uuid4,
                                               editable=False)

    student = models.ForeignKey('students.Student', verbose_name=_('student'),
                                related_name='period_registrations')
    # period = models.ForeignKey('Period', verbose_name=_('period'),
    #                            related_name='studentregistration')
    # suspension_type = models.CharField(
    #     max_length=1, choices=SUSPENSION_TYPE, default=NORMAL)
    DISCIPLINARY = 'DS'
    EXCEPTION = 'ES'
    NORMAL = 'NS'
    SUSPENSION_TYPE = (
        (DISCIPLINARY, _('Disciplinary Suspension ')),
        (EXCEPTION, _('Exceptional Suspension')),
        (NORMAL, _('Normal Suspension')),
    )
    REGISTERED = 'R'
    # SUSPENDED = 'S'
    DROPPED = 'D'  # منطقع
    REGISTRATION_NOT_COMPLETED = 'RNC'
    REGISTRATION_TYPE = (
        (_('Suspended'), SUSPENSION_TYPE),
        (REGISTERED, _('Registered')),
        (DROPPED, _('Dropped Out')),
        (REGISTRATION_NOT_COMPLETED, _('Registration not completed')),
    )

    registration_type = models.CharField(
        max_length=3, choices=REGISTRATION_TYPE,
        default=REGISTRATION_NOT_COMPLETED)

    period = models.ForeignKey('periods.Period')

    section_enrolments = models.ManyToManyField('courses.Section',
                                                through=SectionEnrolment,
                                                blank=True)

    class Meta:
        unique_together = (
            ('student', 'period'),
        )
        ordering = (
            ('student', 'period')
        )

    def __str__(self):
        return '{} {}'.format(self.student, self.period)
