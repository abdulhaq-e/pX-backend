# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers

from .models import Assessment, AssessmentResult


class AssessmentSerialiser(serializers.ModelSerializer):

    included_serializers = {
        'assessment_results': 'pX.administration.courses.assessments.serialisers.AssessmentResultSerialiser'
    }

    class Meta:
        model = Assessment
        fields = ('assessment_type', 'period_course', 'total_grade',
                  'result_status')


class AssessmentResultSerialiser(serializers.ModelSerializer):

    class Meta:
        model = AssessmentResult
        fields = ('assessment', 'section_enrolment', 'grade', 'hidden')
