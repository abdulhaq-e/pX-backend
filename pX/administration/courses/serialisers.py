# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework_json_api import serializers
from rest_framework_json_api.relations import ResourceRelatedField

from .models import Course, Section, PeriodCourse


class CourseSerialiser(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Course
        fields = ('name', 'code')
        #exclude = ('department', 'degrees')


class SectionSerialiser(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Section
        #exclude = ('period_course',)


class PeriodCourseSerialiser(serializers.ModelSerializer):

    assessments = ResourceRelatedField(many=True, read_only=True)
    course = ResourceRelatedField(read_only=True)
    included_serializers = {
        'course': CourseSerialiser,
        'assessments': 'pX.administration.courses.assessments.serialisers.AssessmentSerialiser'
    }

    class Meta:
        model = PeriodCourse
        fields = ('assessments', 'course', 'shared_groups',)
