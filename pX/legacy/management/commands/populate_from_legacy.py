# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import division

import os
import datetime
import time
import codecs

from django.core.management.base import BaseCommand

from tables_handler import (export_tables, prepare_tables)
from administration_handler import (create_departments,
                                    create_degrees,
                                    create_degree_courses)
from courses_handler import create_courses
from students_handler import create_users, assign_advisors
from summary_handler import create_registrations
from registration_handler import create_enrolments
from fields_handler import fields
from cleaning_up import (exclusions, clean_up_graduates,
                         clean_up_delete_students,  # get_results,
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

    def add_arguments(self, parser):

        update_or_fresh = parser.add_mutually_exclusive_group(required=True)
        update_or_fresh.add_argument(
            '--update',
            action='store_true')
        update_or_fresh.add_argument(
            '--fresh',
            action='store_true')

        # migration_files = parser.add_mutually_exclusive_group(required=True)
        # migration_files.add_argument(
        #     '--use-latest',
        #     action='store_true',
        #     dest='use_latest')
        # migration_files.add_argument(
        #     '--migration')
        # migration_files.add_argument(
        #     '--raw',
        #     action='store_true')
        parser.add_argument('--init',
                            action='store_true',
                            dest='init',
                            default=False,
                            help='initialise migration')
        parser.add_argument('--do-it-all',
                            action='store_true',
                            dest='do-it-all',
                            default=False,
                            help='Run everything!')
        parser.add_argument('--export-and-prepare-tables',
                            action='store_true',
                            dest='export-and-prepare-tables',
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

    def _export_tables(self, config):
        export_tables(config)

    def _prepare_tables(self, config):
        prepare_tables(config)

    def _create_departments(self, config):
        create_departments(config)

    def _create_courses(self, config):
        create_courses(config)

    def _create_users(self, config):
        create_users(config)

    def _create_registration(self, config):
        create_registrations(config)

    def _create_enrolments(self, config):
        create_enrolments(config)

    def _create_degrees(self, config):
        create_degrees(config)

    def _create_degree_courses(self):
        create_degree_courses()

    def _assign_advisors(self, config):
        assign_advisors(config)

    def _create_employees(self):
        create_employees(self)

    def _clean_up(self, file, simulate):
        # get_results()
        clean_up_transferred(file, simulate)
        clean_up_graduates(file, simulate)
        clean_up_delete_students(file, simulate)
        clean_up_left(file, simulate)
        correct_gender(file)
        clean_up_dropped_out_students(file, simulate)
        clean_up_course_names()
        clean_up_equalled_courses()
        # file.close()

    def _export_and_prepare(self, config):
        self._export_tables(config)
        self._prepare_tables(config)

    def _do_it_all(self, simulate):
        self._export_tables(self)
        self._clean_tables(self)
        self._create_departments(self)
        self._create_courses(self)
        self._create_users(self)
        self._create_degrees(self)
        self._create_registration(self)
        self._create_enrolments(self)
        self._clean_up(self)
        self._assign_advisors(self)

    def handle(self, *args, **options):
        self.verbosity = options.get('verbosity')
        self.simulate = options.get('simulate')

        BASE = '../pX-tools/legacyDB/'
        BASE_MIGRATIONS_DIR = os.path.join(
            BASE, 'migrations')

        if options['init']:
            time_now = datetime.datetime.now()
            time_stamp = time.mktime(time_now.timetuple())

            migration_type = 'update' if options['update'] else 'fresh'
            migration_name = "{}-({})".format(time_stamp, migration_type)
        elif not options['init']:
            all_migrations = os.listdir(BASE_MIGRATIONS_DIR)
            migration_name = sorted(all_migrations)[-1]

        BASE_MIGRATION_DIR = os.path.join(
            BASE_MIGRATIONS_DIR, migration_name)
        EXPORTED_FILES_LOCATION = os.path.join(
            BASE_MIGRATION_DIR, 'exported')
        PREPARED_FILES_LOCATION = os.path.join(
            BASE_MIGRATION_DIR, 'prepared')
        LOGS_FILES_LOCATION = os.path.join(
            BASE_MIGRATION_DIR, 'logs')

        DIRECTORIES = [BASE_MIGRATION_DIR,
                       EXPORTED_FILES_LOCATION,
                       PREPARED_FILES_LOCATION,
                       LOGS_FILES_LOCATION
                       ]

        if options['init']:
            for directory in DIRECTORIES:
                if not os.path.exists(directory):
                    os.makedirs(directory)
            with open(
                os.path.join(
                    BASE_MIGRATION_DIR,
                    'info.txt'), 'w') as info:
                info.write(str(time_now))
            if self.verbosity > 1:
                print('Created migration {}, {}'
                      .format(migration_name, str(time_now)))
        elif not options['init']:
            for directory in DIRECTORIES:
                assert os.path.exists(directory)

        CONFIG = {
            'FILES': self.FILES,
            'TABLES': self.TABLES,
            'MDE_FILE_LOCATION': BASE,
            'EXPORTED_FILES_LOCATION': EXPORTED_FILES_LOCATION,
            'PREPARED_FILES_LOCATION': PREPARED_FILES_LOCATION,
            'LOGS_FILES_LOCATION': LOGS_FILES_LOCATION,
            'VERBOSITY': self.verbosity,
            'FIELDS': fields(),
            'EXCLUSIONS': exclusions()
        }
        if options['do-it-all']:
            self._do_it_all(options)
        if options['employees']:
            self._create_employees(self)
        if options['export-and-prepare-tables']:
            self._export_and_prepare(CONFIG)
        if options['students']:
            self._create_users(CONFIG)
        if options['courses']:
            self._create_departments(CONFIG)
            self._create_courses(CONFIG)
        if options['registrations']:
            self._create_degrees(CONFIG)
            self._create_registration(CONFIG)
        if options['enrolments']:
            self._create_enrolments(CONFIG)
        if options['cleanup']:
            f = codecs.open(LOGS_FILES_LOCATION + '/' + 'cleaning_up.txt', 'w', 'utf-8')
            self._clean_up(f, options['simulate'])
        if options['degree-courses']:
            self._create_degree_courses(CONFIG)
        if options['assign-advisors']:
            self._assign_advisors(CONFIG)
