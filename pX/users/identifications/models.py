from __future__ import unicode_literals

from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from ...base.models import pXBaseModel


class NationalID(pXBaseModel):
    """
    """
    #person = models.ForeignKey(Person)
    national_id = models.CharField(max_length=255)

    class Meta:
        pass


class PersonalID(pXBaseModel):
    """
    """
    #person = models.ForeignKey(Person)
    id_number = models.CharField(max_length=255)
    issue_date = models.DateField()
    expiry_date = models.DateField()
    place_of_issuing = models.CharField(max_length=255)

    class Meta:
        pass


class PassportID(pXBaseModel):
    """
    """

    #person = models.ForeignKey(Person)
    passport_number = models.CharField(max_length=255)
    issue_date = models.DateField()
    expiry_date = models.DateField()

    class Meta:
        pass


class Identification(pXBaseModel):
    """
    """
    identification_type = models.ForeignKey(ContentType)

    class Meta:
        pass


class PersonID(pXBaseModel):
    """
    """

    identification = models.ForeignKey('Identification')
    person = models.ForeignKey('users.Person')
    content_object = GenericForeignKey('content_type', 'object_id')
    content_type = models.ForeignKey(ContentType)
    object_id = models.CharField(max_length=255)

    class Meta:
        pass
