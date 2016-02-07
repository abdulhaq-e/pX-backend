# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import viewsets
from .models import Period
from .serialisers import PeriodSerialiser


class PeriodViewSet(viewsets.ModelViewSet):

    model = Period
    serializer_class = PeriodSerialiser
    queryset = Period.objects.all()
