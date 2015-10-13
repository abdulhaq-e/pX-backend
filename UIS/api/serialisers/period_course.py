# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers

from UIS.models.courses import PeriodCourse

from .section import SectionSerialiser
from .course import CourseSerialiser


class PeriodCourseSectionSerialiser(serializers.ModelSerializer):

    course = CourseSerialiser(read_only=True)
    main_section = SectionSerialiser(source='section_set', many=True)

    class Meta:
        model = PeriodCourse
