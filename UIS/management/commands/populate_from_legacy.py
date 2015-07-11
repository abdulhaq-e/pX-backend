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
from UIS.models.courses import CourseCatalogue
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
from UIS.models.administration import Department
from UIS.models.courses import (CourseCatalogue,
                                Section)
from UIS.models.users import UISUser, UserProfile, Employee
from UIS.models.degrees import Degree, DegreeCourse

import re

from courses_handler import (courses_table_read,
                             courses_table_write,
                             courses_table_process)
from students_handler import (students_table_read,
                              students_table_write,
                              students_table_process)
from registration_handler import (registration_table_read,
                                  registration_table_write,
                                  registration_table_process)
from summary_handler import (summary_table_read,
                             summary_table_write,
                             summary_table_process)
from departments_handler import (departments_table_read,
                                 departments_table_write,
                                 departments_table_process)


class Command(BaseCommand):
    args = '<foo bar ...>'
    help = 'our help string comes here'

    FILES = ['Register.mde', 'DBArchive.MDE']

    TABLES = {'DEPTS': 'departments',
              'Students': 'students',
              'Courses': 'courses',
              'Register': 'registration',
              'Summary': 'summary'}
    #'Register1': 'periods'}

    FILES_LOCATION = 'legacyDB/'
    EXPORTED_FILES_LOCATION = FILES_LOCATION + 'exported/'
    PREPARED_FILES_LOCATION = FILES_LOCATION + 'prepared/'
    CONFLICTS_FILES_LOCATION = FILES_LOCATION + 'conflicts/'
    FIELDS = dict(
        [
            ('exported_read_fields', dict(
                [
                    ('DEPARTMENTS', [None, 'name_ar', 'name']),
                    ('COURSES', ['code', 'name', 'name_ar', None,
                                 'department', 'credit', None,
                                 None, None, None, None, None,
                                 None, None, None, None, None,
                                 None, None]),
                    ('STUDENTS', ['registration_number', 'first_name_ar',
                                  None, None, None, None,
                                  None, None, None,
                                  'first_name', None]),
                    ('REGISTRATION', ['registration_number',
                                      None, None, None,
                                      'period', None, 'code',
                                      'group', 'grade',
                                      'added_or_dropped',
                                      'credit',
                                      None, None, None,
                                      None, None, None,
                                      None, None, None,
                                      None, None, None,
                                      None, 'registration_type',
                                      None, 'status', None, None,
                                      None, None, None]),
                    ('SUMMARY', ['registration_number', 'period',
                                 'registration_type']),
                ])
            ),
            ('prepared_write_fields', dict(
                [
                    ('DEPARTMENTS', ['name_ar', 'name']),
                    ('COURSES', ['code', 'name_ar', 'name', 'department',
                                 'credit']),
                    ('STUDENTS', ['registration_number', 'first_name_ar',
                                  'last_name_ar', 'first_name', 'last_name']),
                    ('REGISTRATION', ['registration_number',
                                      'period',
                                      'academic_year',
                                      'code',
                                      'credit',
                                      'group',
                                      'grade',
                                      'registration_type',
                                      'added_or_dropped',
                                      'status']),
                    ('SUMMARY', ['registration_number',
                                 'period', 'academic_year',
                                 'registration_type'])
                ])
            ),
            ('process_fields', dict(
                [
                    ('DEPARTMENTS', ['name_ar', 'name']),
                    ('COURSES', ['code', 'name_ar', 'name',
                                 'department', 'credit']),
                    ('STUDENTS', ['registration_number',
                                  'first_name_ar', 'last_name_ar',
                                  'first_name', 'last_name']),
                    ('SUMMARY', ['registration_number',
                                 'period', 'academic_year',
                                 'registration_type']),
                    ('REGISTRATION', ['registration_number', 'period',
                                      'academic_year', 'code', 'credit',
                                      'group', 'grade', 'registration_type',
                                      'added_or_dropped', 'status'])
                ])
            ),
        ]
    )

    def add_arguments(self, parser):
        parser.add_argument('--do-it-all',
                            action='store_true',
                            dest='do-it-all',
                            default=False,
                            help='Run everything!')
        parser.add_argument('--export-tables',
                            action='store_true',
                            dest='export-tables',
                            default=False,
                            help='Export tables from legacy.')
        parser.add_argument('--clean-tables',
                            action='store_true',
                            dest='clean-tables',
                            default=False,
                            help='Clean exported tables.')
        parser.add_argument('--employees',
                            action='store_true',
                            dest='employees',
                            default=False,
                            help='Create employees.')

    def _export_tables(self):
        # self.FILES += ['airRegister.mde', 'air_Register.mde']
        for f in self.FILES:
            for table in self.TABLES:
                exported_file = (
                    self.EXPORTED_FILES_LOCATION + self.TABLES[table] +
                    '_' + f[:-4] + '.csv'
                )
                mde_file = (
                    self.FILES_LOCATION + f
                )
                check_call(['mdb-export', '-H', mde_file, table],
                           stdout=open(exported_file, 'w'))
                if self.verbosity > 1:
                    print('Exported table {} from file {} and'
                          ' exported to {}'.format(self.TABLES[table],
                                                   mde_file,
                                                   exported_file)
                    )

    def _clean_tables(self):
        # self.FILES += ['airRegister.mde', 'air_Register.mde']

        for f in self.FILES:
            for table in self.TABLES:
                exported_file = (
                    self.EXPORTED_FILES_LOCATION + self.TABLES[table] +
                    '_' + f[:-4] + '.csv'
                )
                prepared_file = (
                    self.PREPARED_FILES_LOCATION + self.TABLES[table] +
                    '_' + f[:-4] + '.csv'
                )
                rows = []
                if self.TABLES[table] == 'departments':
                    departments_table_read(
                        exported_file,
                        self.FIELDS['exported_read_fields']['DEPARTMENTS'],
                        rows
                    )
                    if self.verbosity > 1:
                        print('Read {}'.format(exported_file))

                    departments_table_write(
                        prepared_file,
                        self.FIELDS['prepared_write_fields']['DEPARTMENTS'],
                        rows
                    )
                    if self.verbosity > 1:
                        print('Prepared file and exported to {}'
                              .format(prepared_file))
                elif self.TABLES[table] == 'courses':
                    courses_table_read(
                        exported_file,
                        self.FIELDS['exported_read_fields']['COURSES'],
                        rows
                    )
                    if self.verbosity > 1:
                            print('Read {}'.format(exported_file))
                    courses_table_write(
                        prepared_file,
                        self.FIELDS['prepared_write_fields']['COURSES'],
                        rows
                    )
                    if self.verbosity > 1:
                        print('Prepared file and exported to {}'
                              .format(prepared_file))
                elif self.TABLES[table] == 'students':
                    students_table_read(
                        exported_file,
                        self.FIELDS['exported_read_fields']['STUDENTS'],
                        rows
                    )
                    if self.verbosity > 1:
                        print('Read {}'.format(exported_file))
                    students_table_write(
                        prepared_file,
                        self.FIELDS['prepared_write_fields']['STUDENTS'],
                        rows
                    )
                    if self.verbosity > 1:
                        print('Prepared file and exported to {}'
                              .format(prepared_file))
                elif self.TABLES[table] == 'registration':

                    registration_table_read(
                        exported_file,
                        self.FIELDS['exported_read_fields']['REGISTRATION'],
                        rows
                    )
                    if self.verbosity > 1:
                        print('Read {}'.format(exported_file))

                    registration_table_write(
                        prepared_file,
                        self.FIELDS['prepared_write_fields']['REGISTRATION'],
                        rows
                    )
                    if self.verbosity > 1:
                        print('Prepared file and exported to {}'
                              .format(prepared_file))
                elif self.TABLES[table] == 'summary':

                    summary_table_read(
                        exported_file,
                        self.FIELDS['exported_read_fields']['SUMMARY'],
                        rows
                    )
                    if self.verbosity > 1:
                        print('Read {}'.format(exported_file))

                    summary_table_write(
                        prepared_file,
                        self.FIELDS['prepared_write_fields']['SUMMARY'],
                        rows
                    )
                    if self.verbosity > 1:
                        print('Prepared file and exported to {}'
                              .format(prepared_file))

    def _create_departments(self):
        conflicts_file = (self.CONFLICTS_FILES_LOCATION +
                          'DEPARTMENT_CONFLICTS.txt')
        conflicts = open(conflicts_file, 'w')

        for f in self.FILES:
            prepared_file = (
                self.PREPARED_FILES_LOCATION + 'departments' +
                '_' + f[:-4] + '.csv'
            )
            departments_table_process(
                prepared_file,
                self.FIELDS.get('process_fields').get('DEPARTMENTS'),
                conflicts,
                self.verbosity)
        conflicts.close()

    def _create_courses(self):
        conflicts_file = (self.CONFLICTS_FILES_LOCATION +
                          'COURSE_CONFLICTS.txt')
        conflicts = open(conflicts_file, 'w')

        for f in self.FILES:
            prepared_file = (
                self.PREPARED_FILES_LOCATION + 'courses' +
                '_' + f[:-4] + '.csv'
            )
            courses_table_process(
                prepared_file,
                self.FIELDS.get('process_fields').get('COURSES'),
                conflicts,
                self.verbosity)
        conflicts.close()

    def _create_users(self):
        conflicts_file = (self.CONFLICTS_FILES_LOCATION +
                          'STUDENT_CONFLICTS.txt')
        conflicts = open(conflicts_file, 'w')

        for f in self.FILES:
            prepared_file = (
                self.PREPARED_FILES_LOCATION + 'students' +
                '_' + f[:-4] + '.csv'
            )
            students_table_process(
                prepared_file,
                self.FIELDS.get('process_fields').get('STUDENTS'),
                conflicts,
                self.verbosity)
        conflicts.close()

    def _create_registration(self):
        conflicts_file = (self.CONFLICTS_FILES_LOCATION +
                          'registration_CONFLICTS.txt')

        conflicts = open(conflicts_file, 'w')

        for f in self.FILES:
            prepared_file = (
                self.PREPARED_FILES_LOCATION + 'summary' +
                '_' + f[:-4] + '.csv'
            )
            summary_table_process(
                prepared_file,
                self.FIELDS.get('process_fields').get('SUMMARY'),
                conflicts,
                self.verbosity)
        conflicts.close()

    def _create_enrolments(self):

        conflicts_file = (self.CONFLICTS_FILES_LOCATION +
                          'ENROLMENT_CONFLICTS.txt')
        conflicts = open(conflicts_file, 'w')

        #self.FILES = ['Register.mde']

        for f in self.FILES:
            prepared_file = (
                self.PREPARED_FILES_LOCATION + 'registration' +
                '_' + f[:-4] + '.csv'
            )
            registration_table_process(
                prepared_file,
                self.FIELDS.get('process_fields').get('REGISTRATION'),
                conflicts,
                self.verbosity)
        conflicts.close()

    def _create_degrees(self):
        degree = Degree.objects.get_or_create(
            level='U',
            name='Bachelor of Aeronautical Engineering',
            department=Department.objects.get(pk=1),
            credits_required=152,
        )[0]
        if self.verbosity > 1:
            print('Created degree {}'.format(degree))

    def _create_degree_courses(self):
        degree = Degree.objects.all()[0]
        with open(self.FILES_LOCATION + 'prereqs.csv', 'rb') as csvfile:
            reader = unicodecsv.DictReader(
                csvfile, fieldnames=['code', 'pre1',
                                     'pre2'])
            degree = Degree.objects.all()[0]

            for row in reader:
                course = CourseCatalogue.objects.filter(code=row['code'])[0]
                degree_course, msg = DegreeCourse.objects.get_or_create(
                    degree=degree, course=course)
                if self.verbosity > 1:
                    if msg:
                        print("Got {} and added it to {}"
                              .format(row['code'], degree))
                if row['pre1']:
                    course.prerequisites.add(
                        CourseCatalogue.objects.filter(code=row['pre1'])[0])
                    if self.verbosity > 1:
                        print("Added {} as a prerequisite for {}"
                              .format(row['pre1'], row['code']))
                if row['pre2']:
                    course.prerequisites.add(
                        CourseCatalogue.objects.filter(code=row['pre2'])[0])
                    if self.verbosity > 1:
                        print("Added {} as a prerequisite for {}"
                              .format(row['pre2'], row['code']))

    def _create_employees(self):

        users = [
            {
                'first_name': 'Abdulhaq',
                'last_name': 'Emhemmed',
                'first_name_ar': 'عبدالحق',
                'last_name_ar': 'السعيد امحمد',
                'email': 'abdulhaq.emhemmed@aero.eng.uot.edu.ly',
                'password': '12345',
                'username': 'abdulhaq.emhemmed'
            },
            {
                'first_name': 'Ahmed',
                'last_name': 'Almakhlofy',
                'first_name_ar': 'أحمد',
                'last_name_ar': 'المخلوفي',
                'email': 'ahmed@aero.eng.uot.edu.ly',
                'password': '12345',
                'username': 'ahmed'
            },
            {
                'first_name': 'Adel',
                'last_name': 'Kurban',
                'first_name_ar': 'عادل',
                'last_name_ar': 'كربان',
                'email': 'kurban@aero.eng.uot.edu.ly',
                'password': '12345',
                'username': 'kurban'
            },
            {
                'first_name': 'Ashraf',
                'last_name': 'Omar',
                'first_name_ar': 'أشرف',
                'last_name_ar': 'عمر',
                'email': 'ashraf@aero.eng.uot.edu.ly',
                'password': '12345',
                'username': 'ashraf'
            }
        ]

        for a in users:
            try:
                employee = Employee.objects.get(
                    username=a['username'],
                    department=Department.objects.get(name__icontains='aero'))
            except Employee.DoesNotExist:
                employee = Employee.objects.create(
                    username=a['username'],
                    department=Department.objects.get(name__icontains='aero'),
                    first_name=a['first_name'],
                    last_name=a['last_name'],
                    first_name_ar=a['first_name_ar'],
                    last_name_ar=a['last_name_ar'])
                if self.verbosity > 1:
                    print ('Created employee {}'
                           .format(employee))
            if a['username'] == 'abdulhaq.emhemmed':
                try:
                    user = UISUser.objects.get(
                        email='aaa@aaa.com'
                    )
                except UISUser.DoesNotExist:
                    user = UISUser.objects.create_superuser(
                        email='aaa@aaa.com',
                        password='123')
                    if self.verbosity > 1:
                        print('Created superuser {}'
                              .format(user.email))
                try:
                    user_profile = UserProfile.objects.get(
                        user=user, profile_id=employee.pk
                    )
                except UserProfile.DoesNotExist:
                    user_profile = UserProfile.objects.create(
                        user=user, profile=employee
                    )
            try:
                user = UISUser.objects.get(
                    email=a['username']+'@aero.eng.uot.edu.ly'
                )
            except UISUser.DoesNotExist:
                user = UISUser.objects.create(
                    email=a['username']+'@aero.eng.uot.edu.ly',
                    password='12345')
                if self.verbosity > 2:
                    print('Created user {}'
                          .format(user.email))
            try:
                user_profile = UserProfile.objects.get(
                    user=user, profile_id=employee.pk
                )
            except UserProfile.DoesNotExist:
                user_profile = UserProfile.objects.create(
                    user=user, profile=employee
                )

    def _create_all(self):
        pass

    def _flush_all(self):
        self._delete_faculties()
        self._delete_departments()

    def _do_it_all(self):
        self._export_tables()
        self._clean_tables()
        self._create_departments()
        self._create_courses()
        self._create_users()
        self._create_degrees()
        self._create_registration()
        self._create_enrolments()

    def handle(self, *args, **options):
        self.verbosity = options.get('verbosity')

        if options['do-it-all']:
            self._do_it_all()
        if options['employees']:
            self._create_employees()
