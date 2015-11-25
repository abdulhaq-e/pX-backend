# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import viewsets, permissions

from UIS.models.users import UISUser
from ..serialisers.user import UserSerialiser

from oauth2_provider.ext.rest_framework import TokenHasReadWriteScope
# , TokenHasScope


class UserViewSet(viewsets.ModelViewSet):

    serializer_class = UserSerialiser
    queryset = UISUser.objects.all()
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]

    #renderer_class = (JSONRenderer,)
