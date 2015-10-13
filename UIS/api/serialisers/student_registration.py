# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers

from UIS.models.students import StudentRegistration


class StudentRegistrationSerialiser(serializers.HyperlinkedModelSerializer):

    # period_degree = PeriodDegreeSerialiser()
    period = serializers.CharField(source='period_degree.period')
    # student = StudentSerialiser()
    #     source='student_registration.student')
    class Meta:
        model = StudentRegistration
        fields = ('url', 'period', 'registration_type', 'student',)
        # extra_kwargs = {
        #     'url': {'lookup_field': 'enrolment_id'}
        # }
        #exclude = ('period_degree',)
        #read_only_fields = ('section', 'student_registration')
