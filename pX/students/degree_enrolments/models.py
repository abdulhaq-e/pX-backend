# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import uuid

from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from ...base.models import pXBaseModel


class DegreeTransfer(pXBaseModel):

    degree_transfer_id = models.UUIDField(primary_key=True,
                                          default=uuid.uuid4,
                                          editable=False)
    previous_degree = models.ForeignKey("degrees.Degree",
                                        on_delete=models.PROTECT,
                                        related_name="previous_students")
    degree = models.ForeignKey("degrees.Degree")
    student = models.ForeignKey("students.Student")
    period = models.ForeignKey("periods.Period")


class DegreeOriginalEnrolment(pXBaseModel):

    degree_original_id = models.UUIDField(primary_key=True,
                                          default=uuid.uuid4,
                                          editable=False)
    degree = models.ForeignKey("degrees.Degree")
    student = models.ForeignKey("students.Student")
    period = models.ForeignKey("periods.Period")


class DegreeMajorEnrolment(pXBaseModel):

    degree_major_id = models.UUIDField(primary_key=True,
                                       default=uuid.uuid4,
                                       editable=False)
    previous_degree = models.ForeignKey("degrees.Degree",
                                        on_delete=models.PROTECT,
                                        related_name="majored_students")
    degree = models.ForeignKey("degrees.Degree")
    student = models.ForeignKey("students.Student")
    period = models.ForeignKey("periods.Period")


class DegreeEnrolment(pXBaseModel):

    degree_enrolment_id = models.UUIDField(primary_key=True,
                                           default=uuid.uuid4,
                                           editable=False)

    enrolment_object = GenericForeignKey('enrolment_type', 'enrolment_id')
    enrolment_type = models.ForeignKey(ContentType)
    enrolment_id = models.UUIDField()
