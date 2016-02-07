# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework_json_api import serializers

from .models import Period


class PeriodSerialiser(serializers.ModelSerializer):

    name = serializers.CharField(source='__str__')

    class Meta:
        model = Period
        fields = ('name',)
