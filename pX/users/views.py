# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import viewsets

from .models import Person
from .serialisers import PersonSerialiser

# from oauth2_provider.ext.rest_framework import TokenHasReadWriteScope
# , TokenHasScope

class PersonViewSet(viewsets.ModelViewSet):

    serializer_class = PersonSerialiser
    queryset = Person.objects.all()

# class UserViewSet(viewsets.ModelViewSet):
#
#     serializer_class = UserSerialiser
#     queryset = UISUser.objects.all()
#     permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]

    #renderer_class = (JSONRenderer,)
