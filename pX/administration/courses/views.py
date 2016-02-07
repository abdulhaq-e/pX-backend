# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import viewsets

from .models import Course, Section, PeriodCourse
from .serialisers import (CourseSerialiser, SectionSerialiser,
                          PeriodCourseSerialiser)
from .filters import PeriodCourseFilter


class CourseViewSet(viewsets.ModelViewSet):

    model = Course
    serializer_class = CourseSerialiser
    queryset = Course.objects.filter(code='AE302')


class SectionViewSet(viewsets.ModelViewSet):

    model = Section
    serializer_class = SectionSerialiser
    queryset = Section.objects.all()


class PeriodCourseViewSet(viewsets.ModelViewSet):

    model = PeriodCourse
    serializer_class = PeriodCourseSerialiser
    queryset = PeriodCourse.objects.all()
    filter_class = PeriodCourseFilter
