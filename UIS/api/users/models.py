from django.db import models
from django.contrib.auth.models import (BaseUserManager,
                                        AbstractBaseUser,
                                        PermissionsMixin
)

from django.core import validators
from django.utils.translation import ugettext_lazy as _
from django.utils import translation
from django_countries.fields import CountryField
from linguo.models import MultilingualModel
from linguo.managers import MultilingualManager
from django.core.urlresolvers import reverse
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation

import uuid
from UIS.models.base_model import UISBaseModel
from pX import settings
#from gm2m import GM2MField
#from django.contrib.contenttypes.fields import GenericForeignKey
#from django.contrib.contenttypes.models import ContentType

# from UIS.models.roles import Role


class UISUserManager(BaseUserManager, MultilingualManager):

    use_in_migrations = True

    def _create_user(self, email, password, is_staff,
                     is_superuser, **extra_fields):
        """
        Creates and saves a User with the given email name.
        """
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        user = self.model(email=email, is_staff=is_staff,
                          is_active=True, is_superuser=is_superuser,
                          **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, **extra_fields):
        return self._create_user(email, password, False, False,
                                 **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, True,
                                 **extra_fields)

    def get_or_create_user(self, email, password, **extra_fields):
        try:
            return self.get(email=email), False
        except self.model.DoesNotExist:
            return self._create_user(email, password, False, False,
                                     **extra_fields), True


class UISUser(MultilingualModel, AbstractBaseUser,
              UISBaseModel, PermissionsMixin):
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

    roles = models.ManyToManyField('Role', through='UserRole')

    objects = UISUserManager()

    USERNAME_FIELD = 'email'

    class Meta:
        app_label = 'UIS'

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

    def __unicode__(self):
        return self.email


class Person(MultilingualModel, UISBaseModel):
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

    gender = models.CharField(max_length=1, choices=GENDER, null=True)
    nationality = CountryField(default='LY', null=True)
    identifications = models.ManyToManyField('Identification',
                                             through='PersonID')
    address = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        app_label = 'UIS'
        translate = ('first_name', 'last_name')

    def __unicode__(self):
        """
        """
        return ' '.join([self.first_name_ar, self.last_name_ar])

    def get_full_name_ar(self):
        """
        """
        return unicode(self)

    def get_full_name(self):
        """
        """
        return ' '.join([self.first_name, self.last_name])


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

    department = models.ForeignKey('Department', null=False,
                                   on_delete=models.PROTECT,)

    class Meta:
        app_label = 'UIS'
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

    def __unicode__(self):
        return unicode(self.details)


class UserProfile(UISBaseModel):
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
        app_label = 'UIS'

    def __unicode__(self):
        return ' '.join([unicode(self.profile), self.user.email])
