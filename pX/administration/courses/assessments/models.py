# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import uuid

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from .utils import send_assessment_result_email

from ....base.models import pXBaseModel
from ...courses.models import PeriodCourse
from ....students.section_enrolments.models import SectionEnrolment


@python_2_unicode_compatible
class Assessment(pXBaseModel):
    """
    assessments with a 'type' that needs certification before publishing
    should be set to 'waiting for certification' (changed to 'onhold')
    """

    assessment_id = models.UUIDField(primary_key=True,
                                     default=uuid.uuid4,
                                     editable=False)
    UNPUBLISHED = 'U'
    PUBLISHED = 'P'
    ONHOLD = 'O'

    RESULT_STATUS = (
        (UNPUBLISHED, _('Unpublished')),
        (PUBLISHED, _('Published')),
        (ONHOLD, _('On hold')),
    )
    assessment_type = models.ForeignKey('AssessmentType',
                                        on_delete=models.PROTECT)
    period_course = models.ForeignKey(PeriodCourse,
                                      on_delete=models.PROTECT,
                                      related_name="assessments")
    total_grade = models.FloatField()
    result_status = models.CharField(max_length=1, choices=RESULT_STATUS,
                                     default=UNPUBLISHED)

    def __str__(self):
        return '{} ({})'.format(self.period_course, self.assessment_type)

    class Meta:

        unique_together = ('assessment_type', 'period_course')


@python_2_unicode_compatible
class AssessmentType(pXBaseModel):
    """
    """

    assessment_type_id = models.UUIDField(primary_key=True,
                                          default=uuid.uuid4,
                                          editable=False)
    assessment_type = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.assessment_type


@python_2_unicode_compatible
class AssessmentResult(pXBaseModel):
    """
    """

    assessment_grade_id = models.UUIDField(primary_key=True,
                                           default=uuid.uuid4,
                                           editable=False)
    assessment = models.ForeignKey(Assessment,
                                   on_delete=models.PROTECT,
                                   related_name='assessment_results')
    section_enrolment = models.ForeignKey(SectionEnrolment,
                                          related_name='assessment_results')
    grade = models.FloatField(null=True,
                              # validators=[AssessmentGradeValidator()])
                              )
    _grade = models.FloatField(null=True)
    hidden = models.BooleanField(default=False)

    def send_email(self):
        send_assessment_result_email(self)

    def __str__(self):
        return '{} ({} : {})'.format(self.section_enrolment,
                                     self.assessment,
                                     self._grade)

    class Meta:

        unique_together = ('assessment', 'section_enrolment')
