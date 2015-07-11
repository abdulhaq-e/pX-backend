from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from UIS.models.base_model import UISBaseModel
from UIS.models.users import Person


class NationalID(UISBaseModel):
    """
    """
    #person = models.ForeignKey(Person)
    national_id = models.CharField(max_length=255)

    class Meta:
        app_label = 'UIS'


class PersonalID(UISBaseModel):
    """
    """
    #person = models.ForeignKey(Person)
    id_number = models.CharField(max_length=255)
    issue_date = models.DateField()
    expiry_date = models.DateField()
    place_of_issuing = models.CharField(max_length=255)

    class Meta:
        app_label = 'UIS'


class PassportID(UISBaseModel):
    """
    """

    #person = models.ForeignKey(Person)
    passport_number = models.CharField(max_length=255)
    issue_date = models.DateField()
    expiry_date = models.DateField()

    class Meta:
        app_label = 'UIS'


class Identification(UISBaseModel):
    """
    """
    identification_type = models.ForeignKey(ContentType)

    class Meta:
        app_label = 'UIS'


class PersonID(UISBaseModel):
    """
    """

    identification = models.ForeignKey('Identification')
    person = models.ForeignKey(Person)
    content_object = GenericForeignKey('content_type', 'object_id')
    content_type = models.ForeignKey(ContentType)
    object_id = models.CharField(max_length=255)

    class Meta:
        app_label = 'UIS'
