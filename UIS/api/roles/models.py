# *-*
from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _
# from django.contrib.contenttypes.fields import GenericForeignKey
# from django.contrib.contenttypes.models import ContentType
#from UIS.models.users import UISUser
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from UIS.models.base_model import UISBaseModel

from linguo.models import MultilingualModel
#from UIS.models.users import UISUser
from pX import settings

import uuid

class Role(MultilingualModel, UISBaseModel):
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
    role = models.CharField(max_length=100, unique=True)

    class Meta:
        app_label = 'UIS'
        translate = ('role', )

    def __unicode__(self):
        return self.role


class UserRole(UISBaseModel):

    user = models.ForeignKey(settings.base.AUTH_USER_MODEL)
    role = models.ForeignKey('Role')
    content_object = GenericForeignKey('content_type', 'object_id')
    content_type = models.ForeignKey(ContentType)
    object_id = models.UUIDField()

    class Meta:
        app_label = 'UIS'
        unique_together = (('user', 'role', 'object_id'))

    def __unicode__(self):
        return ' '.join([unicode(self.user),
                         unicode(self.role),
                         unicode(self.content_object)
        ])
