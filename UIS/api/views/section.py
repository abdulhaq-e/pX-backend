# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import viewsets

from UIS.models.courses import Section
from ..serialisers.section import SectionSerialiser


class SectionViewSet(viewsets.ModelViewSet):

    model = Section
    serializer_class = SectionSerialiser
    queryset = Section.objects.all()
