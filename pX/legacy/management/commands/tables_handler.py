# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from subprocess import check_call

from .departments_handler import (departments_table_read,
                                  departments_table_write)
from .courses_handler import (courses_table_read,
                              courses_table_write)
from .students_handler import (students_table_read,
                               students_table_write)
from .registration_handler import (registration_table_read,
                                   registration_table_write)

from .summary_handler import (summary_table_read,
                              summary_table_write)


def export_tables(config):
    # files += ['airRegister.mde', 'air_Register.mde']
    files = config['FILES']
    tables = config['TABLES']
    files_location = config['MDE_FILE_LOCATION']
    exported_files_location = config['EXPORTED_FILES_LOCATION']
    verbosity = config['VERBOSITY']

    for f in files:
        for table in tables:
            exported_file = (
                exported_files_location + '/' + tables[table] +
                '_' + f[:-4] + '.csv'
            )
            mde_file = (
                files_location + f
            )
            print(mde_file)
            check_call(['mdb-export', '-H', mde_file, table],
                       stdout=open(exported_file, 'w'))
            if verbosity > 1:
                print('Read table {} from file {} and'
                      ' exported to {}'.format(tables[table],
                                               mde_file,
                                               exported_file)
                      )


def prepare_tables(config):

    files = config['FILES']
    tables = config['TABLES']
    # files_location = config['files_location']
    exported_files_location = config['EXPORTED_FILES_LOCATION']
    prepared_files_location = config['PREPARED_FILES_LOCATION']
    verbosity = config['VERBOSITY']

    for f in files:
        for table in tables:
            exported_file = (
                exported_files_location + '/' + tables[table] +
                '_' + f[:-4] + '.csv'
            )
            prepared_file = (
                prepared_files_location + '/' + tables[table] +
                '_' + f[:-4] + '.csv'
            )
            rows = []
            if tables[table] == 'departments':
                departments_table_read(
                    exported_file,
                    config['FIELDS'][f]['exported_read_fields']['DEPARTMENTS'],
                    rows
                )
                if verbosity > 1:
                    print('Read {}'.format(exported_file))

                departments_table_write(
                    prepared_file,
                    config['FIELDS'][f]['prepared_write_fields']['DEPARTMENTS'],
                    rows
                )
                if verbosity > 1:
                    print('Prepared file and exported to {}'
                          .format(prepared_file))
            elif tables[table] == 'courses':
                courses_table_read(
                    exported_file,
                    config['FIELDS'][f]['exported_read_fields']['COURSES'],
                    rows
                )
                if verbosity > 1:
                        print('Read {}'.format(exported_file))
                courses_table_write(
                    prepared_file,
                    config['FIELDS'][f]['prepared_write_fields']['COURSES'],
                    rows
                )
                if verbosity > 1:
                    print('Prepared file and exported to {}'
                          .format(prepared_file))
            elif tables[table] == 'students':
                students_table_read(
                    exported_file,
                    config['FIELDS'][f]['exported_read_fields']['STUDENTS'],
                    rows
                )
                if verbosity > 1:
                    print('Read {}'.format(exported_file))
                students_table_write(
                    prepared_file,
                    config['FIELDS'][f]['prepared_write_fields']['STUDENTS'],
                    rows, f, config['EXCLUSIONS']
                )
                if verbosity > 1:
                    print('Prepared file and exported to {}'
                          .format(prepared_file))
            elif tables[table] == 'registration':

                registration_table_read(
                    exported_file,
                    config['FIELDS'][f]['exported_read_fields']['REGISTRATION'],
                    rows
                )
                if verbosity > 1:
                    print('Read {}'.format(exported_file))

                registration_table_write(
                    prepared_file,
                    config['FIELDS'][f]['prepared_write_fields']['REGISTRATION'],
                    rows
                )
                if verbosity > 1:
                    print('Prepared file and exported to {}'
                          .format(prepared_file))
            elif tables[table] == 'summary':

                summary_table_read(
                    exported_file,
                    config['FIELDS'][f]['exported_read_fields']['SUMMARY'],
                    rows
                )
                if verbosity > 1:
                    print('Read {}'.format(exported_file))

                summary_table_write(
                    prepared_file,
                    config['FIELDS'][f]['prepared_write_fields']['SUMMARY'],
                    rows
                )
                if verbosity > 1:
                    print('Prepared file and exported to {}'
                          .format(prepared_file))
