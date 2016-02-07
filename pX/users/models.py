# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import uuid

from django.db import models
from django.contrib.auth.models import (AbstractBaseUser,
                                        PermissionsMixin)
from django.core import validators
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation

from django_countries.fields import CountryField

import settings
from .managers import pXUserManager
from ..base.models import pXBaseModel
from .roles.models import UserRole
from .identifications.models import PersonID


@python_2_unicode_compatible
class pXUser(AbstractBaseUser, pXBaseModel, PermissionsMixin):
    """

    """

    user_id = models.UUIDField(primary_key=True,
                               default=uuid.uuid4, editable=False)

    email = models.EmailField(
        verbose_name=_('email address'),
        max_length=255,
        unique=True,
    )

    is_active = models.BooleanField(default=True, null=False)
    is_staff = models.BooleanField(default=False, null=False)

    roles = models.ManyToManyField('roles.Role', through=UserRole)

    objects = pXUserManager()

    USERNAME_FIELD = 'email'

    class Meta:
        pass

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    #def get_absolute_url(self):
        # if self.user_type == 'E':
        #     return reverse('UIS:employee-home',
        #                    kwargs={
        #                        'username': self.employee.username,
        #                    }
        #                )
        # elif self.user_type == 'S':
        #     return reverse('UIS:student-home',
        #                    kwargs={
        #                        'registration_number': self.student.registration_number,
        #                    }
        #             )

    def __str__(self):
        return self.email


@python_2_unicode_compatible
class Person(pXBaseModel):
    """"""
    """"""
    person_id = models.UUIDField(primary_key=True,
                                 default=uuid.uuid4,
                                 editable=False)
    first_name = models.CharField(max_length=50,
                                  verbose_name=_('first name'))
    last_name = models.CharField(max_length=50,
                                 verbose_name=_('last Name'))
    MALE = 'M'
    FEMALE = 'F'
    GENDER = (
        (MALE, _('Male')),
        (FEMALE, _('Female')),
    )

    date_of_birth = models.DateField(null=True)

    gender = models.CharField(max_length=1, choices=GENDER)
    nationality = CountryField(default='LY')
    identifications = models.ManyToManyField('identifications.Identification',
                                             through=PersonID,
                                             blank=True)
    address = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        pass

    def __str__(self):

        return self.full_name_ar

    @property
    def full_name_ar(self):

        return '{} {}'.format(self.first_name_ar, self.last_name_ar)

    @property
    def full_name(self):

        return '{} {}'.format(self.first_name, self.last_name)


@python_2_unicode_compatible
class Employee(Person):
    """
    similar notes to the common info

    TODO: REVIEW the permission issue

    random thoughts:

    - for some reason, is_staff, is_admin looks completely ugly!
      totally unpythonic! I'm sure there is another solution.
    - THE ABOVE HAS BEEN SOLVED (PARTIALLY)
    """

    employee_id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                                   editable=False)

    details = models.OneToOneField(Person, parent_link=True)
    user = GenericRelation('UserProfile',
                           content_type_field='profile_type',
                           object_id_field='profile_id')
    username = models.CharField(
        _('username'),
        max_length=30,
        help_text=_('Required. 30 characters or fewer. Letters, digits and '
                    '@/./+/-/_ only.'),
        validators=[
            validators.RegexValidator(
                r'^[\w.@+-]+$',
                _('Enter a valid username. '
                  'This value may contain only letters, numbers '
                  'and @/./+/-/_ characters.'), 'invalid'),
        ])

    #objects = CommonInfoManager()

    department = models.ForeignKey('administration.Department', null=False,
                                   on_delete=models.PROTECT,)

    class Meta:
        unique_together = (('username', 'department'))

    # def save(self, *args, **kwargs):

    #     self.email = self.username + '@' + self.department.domain_name

    #     super(Employee, self).save(*args, **kwargs)
    #     # Call the "real" save() method.
    #     ut = UserType.objects.create(content_object=self)
    #     UISUser.objects.create_user(user_type=ut, email=self.email,
    #                            first_name=self.first_name,
    #                            last_name=self.last_name,
    #                            password=self.username)

    def __str__(self):
        return str(self.details)


class UserProfile(pXBaseModel):
    """"""

    """"""
    user_profile_id = models.UUIDField(primary_key=True,
                                       default=uuid.uuid4,
                                       editable=False)

    user = models.OneToOneField(settings.base.AUTH_USER_MODEL)
    profile = GenericForeignKey('profile_type', 'profile_id')
    profile_type = models.ForeignKey(ContentType)
    profile_id = models.UUIDField()

    class Meta:
        pass

    def __unicode__(self):
        return ' '.join([unicode(self.profile), self.user.email])
