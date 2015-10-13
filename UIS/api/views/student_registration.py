# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import viewsets

from UIS.models.students import StudentRegistration
from ..serialisers.student_registration import StudentRegistrationSerialiser


class StudentRegistrationViewSet(viewsets.ModelViewSet):

    model = StudentRegistration
    serializer_class = StudentRegistrationSerialiser
    queryset = StudentRegistration.objects.all()
