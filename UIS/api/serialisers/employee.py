# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

# from rest_framework import serializers

from .person import PersonSerialiser
from UIS.models.users import Employee


class EmployeeSerialiser(PersonSerialiser):

    # student = serializers.HyperlinkedIdentityField(
    #     view_name='student-detail',
    #     lookup_field='student.registration_number',
    # )

    class Meta:
        model = Employee
        # fields = ('student',)
