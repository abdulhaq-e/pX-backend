# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import viewsets

from UIS.models.courses import Course
from ..serialisers.course import CourseSerialiser


class CourseViewSet(viewsets.ModelViewSet):

    model = Course
    serializer_class = CourseSerialiser
    queryset = Course.objects.all()
