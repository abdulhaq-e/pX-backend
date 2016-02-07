# -*- coding: utf-8 -*-

from django.db import models
from django.db.models import F

from .querysets import SectionEnrolmentQuerySet


class SectionEnrolmentManager(models.Manager.from_queryset(
        SectionEnrolmentQuerySet)):
    def get_queryset(self):
        return super(SectionEnrolmentManager, self).get_queryset().annotate(
            code=F('section__period_course__course__code'),
            course=F('section__period_course__course'),
            name=F('section__period_course__course__name'),
            name_ar=F('section__period_course__course__name_ar'),
            group=F('section__group'),
            #grade=self.model.grade,
            credit=F('section__period_course__course__credit'),
            period=F('section__period_course__period')
        )
