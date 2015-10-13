# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

# from rest_framework import serializers

from .person import PersonSerialiser
from .student_registration import StudentRegistrationSerialiser

from UIS.models.students import Student


class StudentSerialiser(PersonSerialiser):

    student_registrations = StudentRegistrationSerialiser(many=True)
    #first_name = serializers.CharField(source='person_ptr.first_name')
    # url = serializers.HyperlinkedIdentityField(
    #     lookup_field='registration_number',
    #     view_name='student-detail'
    # )
    # student_registrations = serializers.PrimaryKeyRelatedField(
    #    source='studentregistration', read_only=True, many=True)
    # periods = serializers.PrimaryKeyRelatedField(
    #     source='periods.student_read_only=True, many=True)


    # lookup_field = 'pk'
    # lookup_url_kwarg = 'id'

    class Meta:
        model = Student

        #exclude = ('details', 'periods')
        fields = ('url', 'first_name_ar', 'last_name_ar',
                  'first_name', 'last_name', 'registration_number',
                  'full_name_ar', 'full_name', 'student_registrations',)
        # extra_kwargs = {
        #     'url': {'lookup_field': 'registration_number'}
        # }
