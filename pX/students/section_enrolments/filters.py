# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

import django_filters

from ..enrolments.models import SectionEnrolment


class SectionEnrolmentFilter(django_filters.FilterSet):

    registration_number = django_filters.CharFilter(
        name="student_registration__student__registration_number")

    student = django_filters.CharFilter(
        name="student_registration__student")

    class Meta:
        model = SectionEnrolment
        fields = ('registration_number', 'student')
