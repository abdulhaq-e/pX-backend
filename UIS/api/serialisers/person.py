# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers

from UIS.models.users import Person


class PersonSerialiser(serializers.HyperlinkedModelSerializer):

    full_name_ar = serializers.CharField(source='get_full_name_ar')
    full_name = serializers.CharField(source='get_full_name')

    class Meta:
        model = Person
        fields = ('url', 'first_name_ar', 'last_name_ar',
                  'first_name', 'last_name',
                  'full_name_ar', 'full_name')
