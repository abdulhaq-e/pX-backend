# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import viewsets

from UIS.models.users import UISUser
from ..serialisers.user import UserSerialiser


class UserViewSet(viewsets.ModelViewSet):

    serializer_class = UserSerialiser
    queryset = UISUser.objects.all()
    #renderer_class = (JSONRenderer,)
