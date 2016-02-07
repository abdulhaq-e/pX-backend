# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import division

from copy import deepcopy
import codecs

import uuid
from django.core.urlresolvers import reverse
from collections import OrderedDict
#from UIS.querysets import StudentEnrolmentQuerySet

from django.core.management.base import BaseCommand
from django.db import IntegrityError
import random
from subprocess32 import check_call
import unicodecsv
from ....administration.models import Department
from ....users.models import pXUser, UserProfile, Employee
from ....administration.degrees.models import Degree
from ....administration.courses.models import (CoursePrerequisite,
                                               DegreeCourse)
from ....students.models import Student

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
from general_handlers import registration_number_handler

from fields_handler import fields
from cleaning_up import (exclusions, clean_up_graduates,
                         clean_up_delete_students, get_results,
                         correct_gender, clean_up_dropped_out_students,
                         clean_up_transferred, clean_up_course_names,
                         clean_up_equalled_courses, clean_up_left)


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

    FILES_LOCATION = '../pX-tools/legacyDB/'
    EXPORTED_FILES_LOCATION = FILES_LOCATION + 'exported/'
    PREPARED_FILES_LOCATION = FILES_LOCATION + 'prepared/'
    CONFLICTS_FILES_LOCATION = FILES_LOCATION + 'conflicts/'
    FIELDS = fields()
    EXCLUSIONS = exclusions()

    def add_arguments(self, parser):
        parser.add_argument('--do-it-all',
                            action='store_true',
                            dest='do-it-all',
                            default=False,
                            help='Run everything!')
        parser.add_argument('--export-and-clean-tables',
                            action='store_true',
                            dest='export-and-clean-tables',
                            default=False,
                            help='Export tables from legacy.')
        parser.add_argument('--employees',
                            action='store_true',
                            dest='employees',
                            default=False,
                            help='Create employees.')
        parser.add_argument('--students',
                            action='store_true',
                            dest='students',
                            default=False,
                            help='Create students.')
        parser.add_argument('--courses',
                            action='store_true',
                            dest='courses',
                            default=False,
                            help='Create courses.')
        parser.add_argument('--registrations',
                            action='store_true',
                            dest='registrations',
                            default=False,
                            help='Create registrations.')
        parser.add_argument('--enrolments',
                            action='store_true',
                            dest='enrolments',
                            default=False,
                            help='Create enrolments.')
        parser.add_argument('--clean-up',
                            action='store_true',
                            dest='cleanup',
                            default=False,
                            help='Clean up.')
        parser.add_argument('--simulate',
                            action='store_true',
                            dest='simulate',
                            default=False,
                            help='Only run a simulation.')
        parser.add_argument('--degree-courses',
                            action='store_true',
                            dest='degree-courses',
                            default=False,
                            help='Create degree courses.')
        parser.add_argument('--assign-advisors',
                            action='store_true',
                            dest='assign-advisors',
                            default=False,
                            help='Assign advisors.')


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
                        self.FIELDS[f]['exported_read_fields']['DEPARTMENTS'],
                        rows
                    )
                    if self.verbosity > 1:
                        print('Read {}'.format(exported_file))

                    departments_table_write(
                        prepared_file,
                        self.FIELDS[f]['prepared_write_fields']['DEPARTMENTS'],
                        rows
                    )
                    if self.verbosity > 1:
                        print('Prepared file and exported to {}'
                              .format(prepared_file))
                elif self.TABLES[table] == 'courses':
                    courses_table_read(
                        exported_file,
                        self.FIELDS[f]['exported_read_fields']['COURSES'],
                        rows
                    )
                    if self.verbosity > 1:
                            print('Read {}'.format(exported_file))
                    courses_table_write(
                        prepared_file,
                        self.FIELDS[f]['prepared_write_fields']['COURSES'],
                        rows
                    )
                    if self.verbosity > 1:
                        print('Prepared file and exported to {}'
                              .format(prepared_file))
                elif self.TABLES[table] == 'students':
                    students_table_read(
                        exported_file,
                        self.FIELDS[f]['exported_read_fields']['STUDENTS'],
                        rows
                    )
                    if self.verbosity > 1:
                        print('Read {}'.format(exported_file))
                    students_table_write(
                        prepared_file,
                        self.FIELDS[f]['prepared_write_fields']['STUDENTS'],
                        rows, f, self.EXCLUSIONS
                    )
                    if self.verbosity > 1:
                        print('Prepared file and exported to {}'
                              .format(prepared_file))
                elif self.TABLES[table] == 'registration':

                    registration_table_read(
                        exported_file,
                        self.FIELDS[f]['exported_read_fields']['REGISTRATION'],
                        rows
                    )
                    if self.verbosity > 1:
                        print('Read {}'.format(exported_file))

                    registration_table_write(
                        prepared_file,
                        self.FIELDS[f]['prepared_write_fields']['REGISTRATION'],
                        rows
                    )
                    if self.verbosity > 1:
                        print('Prepared file and exported to {}'
                              .format(prepared_file))
                elif self.TABLES[table] == 'summary':

                    summary_table_read(
                        exported_file,
                        self.FIELDS[f]['exported_read_fields']['SUMMARY'],
                        rows
                    )
                    if self.verbosity > 1:
                        print('Read {}'.format(exported_file))

                    summary_table_write(
                        prepared_file,
                        self.FIELDS[f]['prepared_write_fields']['SUMMARY'],
                        rows
                    )
                    if self.verbosity > 1:
                        print('Prepared file and exported to {}'
                              .format(prepared_file))

    def _create_departments(self, files):
        conflicts_file = (self.CONFLICTS_FILES_LOCATION +
                          'DEPARTMENT_CONFLICTS.txt')
        conflicts = open(conflicts_file, 'w')

        for file in files:
            prepared_file = (
                self.PREPARED_FILES_LOCATION + 'departments' +
                '_' + file[:-4] + '.csv'
            )
            departments_table_process(
                prepared_file,
                self.FIELDS[file].get('process_fields').get('DEPARTMENTS'),
                conflicts, self.verbosity)

        conflicts.close()

    def _create_courses(self, files):
        conflicts_file = (self.CONFLICTS_FILES_LOCATION +
                          'COURSE_CONFLICTS.txt')
        conflicts = open(conflicts_file, 'w')

        for file in files:
            prepared_file = (
                self.PREPARED_FILES_LOCATION + 'courses' +
                '_' + file[:-4] + '.csv'
            )
            courses_table_process(
                prepared_file,
                self.FIELDS[file].get('process_fields').get('COURSES'),
                conflicts,
                self.verbosity)

        conflicts.close()

    def _create_users(self, files):
        conflicts_file = (self.CONFLICTS_FILES_LOCATION +
                          'STUDENT_CONFLICTS.txt')
        conflicts = open(conflicts_file, 'w')

        for file in files:
            prepared_file = (
                self.PREPARED_FILES_LOCATION + 'students' +
                '_' + file[:-4] + '.csv'
            )
            students_table_process(
                prepared_file,
                self.FIELDS[file].get('process_fields').get('STUDENTS'),
                conflicts,
                self.verbosity)

        conflicts.close()

    def _create_registration(self, files):
        conflicts_file = (self.CONFLICTS_FILES_LOCATION +
                          'registration_CONFLICTS.txt')

        conflicts = open(conflicts_file, 'w')

        for file in files:
            prepared_file = (
                self.PREPARED_FILES_LOCATION + 'summary' +
                '_' + file[:-4] + '.csv'
            )
            summary_table_process(
                prepared_file,
                self.FIELDS[file].get('process_fields').get('SUMMARY'),
                conflicts,
                self.verbosity)

        conflicts.close()

    def _create_enrolments(self, files):

        conflicts_file = (self.CONFLICTS_FILES_LOCATION +
                          'ENROLMENT_CONFLICTS.txt')
        conflicts = open(conflicts_file, 'w')

        #self.FILES = ['Register.mde']

        for file in files:
            prepared_file = (
                self.PREPARED_FILES_LOCATION + 'registration' +
                '_' + file[:-4] + '.csv'
            )
            registration_table_process(
                prepared_file,
                self.FIELDS[file].get('process_fields').get('REGISTRATION'),
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
        with open(self.FILES_LOCATION + 'degree_courses.csv', 'rb') as csvfile:
            reader = unicodecsv.DictReader(
                csvfile, fieldnames=['code', 'pre1',
                                     'pre2'])
            degree = Degree.objects.all()[0]
            for row in reader:
                courses = Course.objects.filter(code=row['code'])
                for c in courses:
                    if (c.code in ['AE325', 'AE200'] and c.credit == 2):
                        continue
                    degree_course = DegreeCourse.objects.filter(
                        degree=degree, course__code=c.code)
                    if not degree_course.exists():
                        DegreeCourse.objects.create(
                            degree=degree, course=c)
                        if self.verbosity > 1:
                            print("Got {} and added it to {}"
                                  .format(row['code'], degree))
                    if row['pre1'] != '':
                        # print row['pre1']
                        CoursePrerequisite.objects.get_or_create(
                            course=c,
                            prerequisite=Course.objects.filter(code=row['pre1'])[0])
                        if self.verbosity > 1:
                            print("Added {} as a prerequisite for {}"
                                  .format(row['pre1'], row['code']))
                    if row['pre2'] != '':
                        CoursePrerequisite.objects.get_or_create(
                            course=c,
                            prerequisite=Course.objects.filter(code=row['pre2'])[0])
                        if self.verbosity > 1:
                            print("Added {} as a prerequisite for {}"
                                  .format(row['pre2'], row['code']))

    def _assign_advisors(self):
        files = ['academic_advisors1.csv', 'academic_advisors2.csv']
        for file in files:
            with open(self.FILES_LOCATION + file, 'rb') as csvfile:
                reader = unicodecsv.DictReader(
                    csvfile, fieldnames=['registration_number',
                                         'student_name', 'advisor'])
                for row in reader:
                    registration_number_handler(row)
                    if self.verbosity > 1:
                            print("I'll now process {}, {}"
                                  .format(row['registration_number'],
                                          row['student_name']))
                    student = Student.objects.get(
                        registration_number=row['registration_number']
                    )
                    student.advisor = row['advisor']
                    student.save()


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
                    user = pXUser.objects.get(
                        email='aaa@aaa.com'
                    )
                except pXUser.DoesNotExist:
                    user = pXUser.objects.create_superuser(
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
                user = pXUser.objects.get(
                    email=a['username']+'@aero.eng.uot.edu.ly'
                )
            except pXUser.DoesNotExist:
                user = pXUser.objects.create(
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

    def _clean_up(self, simulate):
        # get_results()
        file = codecs.open(self.CONFLICTS_FILES_LOCATION + 'cleaning_up',
                           'w', 'utf-8')
        clean_up_transferred(file, simulate)
        clean_up_graduates(file, simulate)
        clean_up_delete_students(file, simulate)
        clean_up_left(file, simulate)
        correct_gender(file)
        clean_up_dropped_out_students(file, simulate)
        clean_up_course_names()
        clean_up_equalled_courses()
        file.close()

    def _export_and_clean(self):
        self._export_tables()
        self._clean_tables()

    def _do_it_all(self, simulate):
        self._export_tables()
        self._clean_tables()
        self._create_departments([self.FILES[0], self.FILES[1]])
        self._create_courses([self.FILES[0], self.FILES[1]])
        self._create_users([self.FILES[0], self.FILES[1]])
        self._create_degrees()
        self._create_registration([self.FILES[0], self.FILES[1]])
        self._create_enrolments([self.FILES[0], self.FILES[1]])
        self._clean_up(simulate)
        self._assign_advisors()

    def handle(self, *args, **options):
        self.verbosity = options.get('verbosity')

        if options['do-it-all']:
            self._do_it_all(options['simulate'])
        if options['employees']:
            self._create_employees()
        if options['export-and-clean-tables']:
            self._export_and_clean()
        if options['students']:
            self._create_users([self.FILES[0], self.FILES[1]])
        if options['courses']:
            self._create_departments([self.FILES[0], self.FILES[1]])
            self._create_courses([self.FILES[0], self.FILES[1]])
        if options['registrations']:
            self._create_degrees()
            self._create_registration([self.FILES[0], self.FILES[1]])
        if options['enrolments']:
            self._create_enrolments([self.FILES[0], self.FILES[1]])
        if options['cleanup']:
            self._clean_up(options['simulate'])
        if options['degree-courses']:
            self._create_degree_courses()
        if options['assign-advisors']:
            self._assign_advisors()
