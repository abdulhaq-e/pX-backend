# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError


class AssessmentGradeValidator(object):

    def __init__(self, grade, total_grade):

        self.grade = grade
        self.total_grade = total_grade

    def __call__(self):  # , value=None):
        if not (0 <= self.grade <= self.total_grade):
            raise ValidationError(
                _('Grade cannot be greater than {} or less than 0'
                  .format(self.total_grade))
            )

# def validate_grade(grade):
#     """
#     """
#     if not(grade):
#         pass
#     else:
#         if grade > 100 or grade < 0:
