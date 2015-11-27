# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

import django_filters

from UIS.models.students import StudentEnrolment


class StudentEnrolmentFilter(django_filters.FilterSet):

    registration_number = django_filters.CharFilter(
        name="student_registration__student__registration_number")

    student = django_filters.CharFilter(
        name="student_registration__student")

    class Meta:
        model = StudentEnrolment
        fields = ('registration_number', 'student')
