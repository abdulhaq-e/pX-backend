# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import viewsets
from UIS.models.time_period import PeriodDegree
from ..serialisers.period_degree import PeriodDegreeSerialiser


class PeriodDegreeViewSet(viewsets.ModelViewSet):

    model = PeriodDegree
    serializer_class = PeriodDegreeSerialiser
    queryset = PeriodDegree.objects.all()
