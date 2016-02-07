# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import uuid

from django.db import models

from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation
# from django.contrib.postgres.fields import JSONField

from ..base.models import pXBaseModel

'''
THIS NOTIFICATION MODEL IS ALL TEMPORARY, I NEED A BETTER SOLUTION

A MUCH BETTER SOL^n
'''


@python_2_unicode_compatible
class Notification(pXBaseModel):
    """

    """
    notification_id = models.UUIDField(primary_key=True,
                                       default=uuid.uuid4,
                                       editable=False)
    notification = GenericForeignKey('content_type', 'object_id')
    content_type = models.ForeignKey(ContentType)
    object_id = models.UUIDField()

    # object_content = JSONField()

    def __str__(self):

        return "Notification for {}".format(self.content_type)
