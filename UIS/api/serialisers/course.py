# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers

from UIS.models.courses import Course


class CourseSerialiser(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Course
        exclude = ('department', 'degrees')
