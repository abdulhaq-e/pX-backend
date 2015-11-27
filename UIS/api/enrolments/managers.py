# -*- coding: utf-8 -*-

from django.db import models
from ..enrolments.querysets import StudentEnrolmentQuerySet


class StudentEnrolmentManager(models.Manager.from_queryset(
        StudentEnrolmentQuerySet)):
    def get_queryset(self):
        return super(StudentEnrolmentManager, self).get_queryset().annotate(
            code=F('section__section_type__period_course__course__code'),
            course=F('section__section_type__period_course__course'),
            name=F('section__section_type__period_course__course__name'),
            name_ar=F('section__section_type__period_course__course__name_ar'),
            group=F('section__group'),
                #GRADE=F('grade'),
            credit=F('section__section_type__period_course__course__credit'),
            period=F('section__section_type__period_course__period')
        )
