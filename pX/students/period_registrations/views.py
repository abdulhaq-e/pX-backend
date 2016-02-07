# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import viewsets

from .models import StudentRegistration
from .serialisers import StudentRegistrationSerialiser


class StudentRegistrationViewSet(viewsets.ModelViewSet):

    model = StudentRegistration
    serializer_class = StudentRegistrationSerialiser
    queryset = StudentRegistration.objects.all()
