# *-*
from __future__ import unicode_literals

import uuid

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

import settings
from ...base.models import pXBaseModel


class Role(pXBaseModel):
    """
    """
    # STUDENT_ADVISER = 'STUDENT_ADVISER'
    # DEPT_HEAD = 'DEPT_HEAD'
    # DEPT_HEAD_OF_LE = 'DEPT_HEAD_OF_LE'
    # DEPT_PA_HEAD = 'DEPT_PA_HEAD'
    # DEPT_PROJECTS_COORD = 'DEPT_PROJECTS_COORD'

    # STUDENT = (
    #     (STUDENT_ADVISER, _('Student Adviser')),
    # )
    # DEPARTMENT = (
    #     (DEPT_HEAD, _('Department Head')),
    #     (DEPT_HEAD_OF_LE,
    #      _('Department Head of Learning and Examination')),
    #     (DEPT_PA_HEAD,
    #      _('Personal assistant to head of department')),
    #     (DEPT_PROJECTS_COORD,
    #      _('Department Projects Coordinator')),
    # )
    # ROLES = (
    #     (_('Student'), STUDENT),
    #     (_('Department'), DEPARTMENT),
    # )
    role_id = models.UUIDField(primary_key=True,
                               default=uuid.uuid4, editable=False)
    role = models.CharField(max_length=100, unique=True)

    class Meta:
        pass

    def __unicode__(self):
        return self.role


class UserRole(pXBaseModel):

    user_role_id = models.UUIDField(primary_key=True,
                                    default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.base.AUTH_USER_MODEL)
    role = models.ForeignKey(Role)
    content_object = GenericForeignKey('content_type', 'object_id')
    content_type = models.ForeignKey(ContentType)
    object_id = models.UUIDField()

    class Meta:
        unique_together = (('user', 'role', 'object_id'))

    def __unicode__(self):
        return ' '.join([unicode(self.user),
                         unicode(self.role),
                         unicode(self.content_object)
        ])
