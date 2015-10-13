# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers

from .student_registration import StudentRegistrationSerialiser
from UIS.models.students import StudentResult


class StudentResultSerialiser(serializers.ModelSerializer):

    student_registration = StudentRegistrationSerialiser()

    class Meta:
        model = StudentResult
