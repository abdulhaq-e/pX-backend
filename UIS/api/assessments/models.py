# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import uuid

from django.db import models
from django.utils.translation import ugettext_lazy as _

# from .validators import AssessmentGradeValidator

from ..base.models import UISBaseModel
from ..courses.models import PeriodCourse
from ..enrolments.models import StudentEnrolment


class Assessment(UISBaseModel):
    """
    assessments with a 'type' that needs certification before publishing
    should be set to 'waiting for certification'
    """

    assessment_id = models.UUIDField(primary_key=True,
                                     default=uuid.uuid4,
                                     editable=False)
    UNPUBLISHED = 'U'
    PUBLISHED = 'P'
    WAITING_FOR_CERTIFICATION = 'W'

    RESULT_STATUS = (
        UNPUBLISHED, _('Unpublished'),
        PUBLISHED, _('Published'),
        WAITING_FOR_CERTIFICATION, _('Waiting for Certification')
    )
    assessment_type = models.ForeignKey('AssessmentType',
                                        null=False,
                                        blank=False,
                                        on_delete=models.PROTECT)
    period_course = models.ForeignKey(PeriodCourse,
                                      null=False, blank=False,
                                      on_delete=models.PROTECT)
    total_grade = models.FloatField()
    result_status = models.CharField(choice=RESULT_STATUS)


class AssessmentType(UISBaseModel):
    """
    """

    assessment_type_id = models.UUIDField(primary_key=True,
                                          default=uuid.uuid4,
                                          editable=False)
    assessment_type = models.CharField(max_length=100)


class AssessmentResult(UISBaseModel):
    """
    """

    assessment_grade_id = models.UUIDField(primary_key=True,
                                           default=uuid.uuid4,
                                           editable=False)
    assessment = models.ForeignKey(Assessment,
                                   null=False,
                                   blank=False)
    student_enrolment = models.ForeignKey(StudentEnrolment)
    grade = models.FloatField(null=True,
                              # validators=[AssessmentGradeValidator()])
                              )
    status = models
