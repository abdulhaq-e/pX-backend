# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import BaseUserManager


class pXUserManager(BaseUserManager):

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
