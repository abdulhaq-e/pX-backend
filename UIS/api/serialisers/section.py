# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers

from UIS.models.courses import Section


class SectionSerialiser(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Section
        #exclude = ('period_course',)
