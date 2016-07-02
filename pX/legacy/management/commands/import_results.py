# -*- coding: utf-8 -*-
from __future__ import division, unicode_literals

from copy import deepcopy
from django.db import models, IntegrityError
from django.utils.translation import ugettext_lazy as _
# from pX import settings
import uuid
from django.core.urlresolvers import reverse
from collections import OrderedDict
from django.db.models import F, Sum

from django.core.management.base import BaseCommand
from django.db import IntegrityError
import random
from subprocess32 import check_call
import unicodecsv
from pX.students.section_enrolments.models import SectionEnrolment
from pX.students.models import Student
from pX.administration.periods.models import Period


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
                  'grade']

    period = Period.objects.filter(period=1, academic_year='2015,2016')

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
                registration_number =  row['registration_number']
                # print(registration_number)
                temp_fix = SectionEnrolment.custom.filter(
                    # period_registration__period=self.period,
                    period_registration__student__registration_number=registration_number,
                    code=code)[0]
                # print("hello")
                temp_res = temp_fix.assessment_results.all().filter(assessment__assessment_type__assessment_type='Total')[0]
                # temp_res = temp_fix.assessment_results.all()[2]
                temp_res._grade = float(row['grade'])
                temp_res.save()
                student = Student.objects.get(registration_number=registration_number)
                student.calculate_results()
                student.generate_form('Enrolment Form')
                student.generate_form('Academic Progress')
                # enrolment = SectionEnrolment.objects.get(
                #     student_registration__student__registration_number=registration_number,
                #     section__section_type__period_course__course__code=code,
                #     student_registration__period_degree__period=self.period)
                # enrolment.grade = row['total']
                # enrolment.carry_marks = row['carry_marks']
                # enrolment.final_exam = row['final_exam']
                # enrolment.save()
                if self.verbosity > 1:
                    print("Added result for student {}. "
                          "Total Grade: {} "
                          .format(
                              registration_number,
                              temp_res.grade)
                    )

    def handle(self, *args, **options):

        self.verbosity = options.get('verbosity')
        if options['simulate']:
            self._simulate_import(options['file'], options['code'])
        else:
            self._import_results(options['file'], options['code'])
