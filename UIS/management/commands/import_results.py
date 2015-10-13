# -*- coding: utf-8 -*-

from __future__ import division
from copy import deepcopy
from django.db import models, IntegrityError
from django.utils.translation import ugettext_lazy as _
from pX import settings
import uuid
from django.core.urlresolvers import reverse
from collections import OrderedDict
#from UIS.querysets import StudentEnrolmentQuerySet
from UIS.validators import validate_grade
from django.db.models import F, Sum
from UIS.managers import StudentEnrolmentManager
from UIS.models.time_period import Period, PeriodDegree
from UIS.models.courses import Course
from UIS.models.users import Person
from django.contrib.contenttypes.fields import GenericRelation
from UIS.models.base_model import UISBaseModel
#from UIS.models.administration import Department
# from UIS.models.courses import Section
# from UIS.models.degrees import Degree
# from UIS.models.employees import Employee
# from UIS.models.time_period import Period
#from UIS.models.users import, UISUser




from django.core.management.base import BaseCommand
from django.db import IntegrityError
import random
from subprocess32 import check_call
import unicodecsv
from UIS.models.students import StudentEnrolment

import re


class Command(BaseCommand):
    args = '<foo bar ...>'
    help = 'our help string comes here'

    def add_arguments(self, parser):
        parser.add_argument('file',
                            help='File that contains the results')
        parser.add_argument('code',
                            help='Course code')
        parser.add_argument('--simulate',
                            action='store_true',
                            dest='simulate',
                            default=False,
                            help='Only simulate the import process!')

    fieldnames = ['registration_number',
                          'name',
                          'carry_marks',
                          'final_exam',
                          'total']
    period = Period.objects.filter(period=2, academic_year='2014,2015')

    def _simulate_import(self, file, code):

        with open(file, 'rb') as csvfile:
            reader = unicodecsv.DictReader(
                csvfile, self.fieldnames)
            next(reader, None)
            count = len(list(reader))

        print("This function read the file {} and will import {} "
              "results to the course {} for the period Spring 2015"
              .format(file, count, code))

    def _import_results(self, file, code):

        with open(file, 'rb') as csvfile:
            reader = unicodecsv.DictReader(
                csvfile, self.fieldnames)
            next(reader, None)
            for row in reader:
                registration_number = '0' + row['registration_number']
                enrolment = StudentEnrolment.objects.get(
                    student_registration__student__registration_number=registration_number,
                    section__section_type__period_course__course__code=code,
                    student_registration__period_degree__period=self.period)
                enrolment.grade = row['total']
                enrolment.carry_marks = row['carry_marks']
                enrolment.final_exam = row['final_exam']
                enrolment.save()
                if self.verbosity > 1:
                    print("Added result for student {}. "
                          "Carry marks: {} "
                          "Final exam: {} "
                          "Total Grade: {} "
                          .format(
                              registration_number,
                              enrolment.carry_marks,
                              enrolment.final_exam,
                              enrolment.grade)
                    )

    def handle(self, *args, **options):

        self.verbosity = options.get('verbosity')
        if options['simulate']:
            self._simulate_import(options['file'], options['code'])
        else:
            self._import_results(options['file'], options['code'])
