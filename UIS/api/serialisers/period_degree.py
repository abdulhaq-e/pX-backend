# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers

from UIS.models.time_period import PeriodDegree


class PeriodDegreeSerialiser(serializers.HyperlinkedModelSerializer):

    period = serializers.CharField()

    class Meta:
        model = PeriodDegree
        exclude = ('degree',)
