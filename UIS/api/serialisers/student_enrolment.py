# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers

from UIS.models.students import StudentEnrolment
from .course import CourseSerialiser


class StudentEnrolmentSerialiser(serializers.HyperlinkedModelSerializer):

    # section = SectionSerialiser()

    course = CourseSerialiser(
        source='section.section_type.period_course.course'
    )

    # registration_number = serializers.StringRelatedField(
    #     source='student_registration.student.registration_number')

    class Meta:
        model = StudentEnrolment
