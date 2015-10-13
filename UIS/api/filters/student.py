# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

import django_filters

from UIS.models.students import Student


class StudentFilter(django_filters.FilterSet):

    registration_number = django_filters.CharFilter()

    class Meta:
        model = Student
        fields = ('registration_number',)
