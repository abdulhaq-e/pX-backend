# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

import django_filters

from .models import PeriodCourse


class PeriodCourseFilter(django_filters.FilterSet):

    # course_code = django_filters.CharFilter()

    class Meta:
        model = PeriodCourse
        fields = ('course__code',)
