# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers

from .models import pXUser


class UserSerialiser(serializers.HyperlinkedModelSerializer):

    profile_id = serializers.UUIDField(source='userprofile.profile.pk',
                                         read_only=True)
    # profile = StudentSerialiser(source='userprofile.profile',
    #                               read_only=True)
    profile_type = serializers.CharField(source='userprofile.profile_type')
    roles = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = pXUser
        fields = ('url', 'email', 'roles', 'profile_type', 'profile_id',)
