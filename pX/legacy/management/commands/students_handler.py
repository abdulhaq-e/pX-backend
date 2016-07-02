# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals

import unicodecsv
from general_handlers import registration_number_handler
# from django.db import IntegrityError
from ....users.models import pXUser, UserProfile
from ....students.models import Student


def students_table_read(file, fieldnames, rows):
    with open(file, 'rb') as csvfile:
        reader = unicodecsv.DictReader(
            csvfile, fieldnames)
        for row in reader:
            row['first_name_ar'], row['last_name_ar'] = (
                row['name_ar'].partition(' ')[0],
                row['name_ar'].partition(' ')[2]
            )
            row['first_name'], row['last_name'] = (
                row['name'].partition(' ')[0],
                row['name'].partition(' ')[2]
            )
            row.pop(None, None)
            row.pop('')
            row.pop('name')
            row.pop('name_ar')
            rows.append(row)


def students_table_write(file, fieldnames, rows, db, exclusions):
    with open(file, 'w') as csvfile:
        writer = unicodecsv.DictWriter(
            csvfile, fieldnames)
        writer.writeheader()
        for row in rows:
            registration_number_handler(row)
            if row['registration_number'] in exclusions[db]['STUDENTS']:
                continue
            if (
                row['registration_number'] in
                exclusions['DUPLICATES']['STUDENTS']
            ):
                continue
            writer.writerow(row)


def students_table_process(file, fieldnames, conflicts, verbosity):

    DUPLICATE_STUDENTS = []

    with open(file, 'rb') as csvfile:
        reader = unicodecsv.DictReader(
            csvfile, fieldnames)
        next(reader, None)
        for row in reader:
            if row['gender'].encode('utf8') == "ذكر":
                row['gender'] = 'M'
            elif row['gender'].encode('utf8') == "أنثى":
                row['gender'] = 'F'
            else:
                row['gender'] = 'M'

            if row['date_of_birth'] == '':
                row['date_of_birth'] = None
            else:
                row['date_of_birth'] = row['date_of_birth'].split(' 00:00:00')[0]
                row['date_of_birth'] = ('19' + row['date_of_birth'][-2:] +
                                        '-' + row['date_of_birth'][:2] + '-' +
                                        row['date_of_birth'][3:5])

            row['archive_reason'] = row['archive_reason'].encode('utf8')
            if row['archive_reason'] == 'اخلاء طرف':
                row['archive_reason'] = 'L'
            elif row['archive_reason'] == 'انتقال الى قسم آخر':
                row['archive_reason'] = 'T'
            elif row['archive_reason'] == 'فصل من الكلية':
                row['archive_reason'] = 'K'
            elif row['archive_reason'] == 'خريج':
                row['archive_reason'] = 'G'
            elif row['archive_reason'] == 'انقطاع':
                row['archive_reason'] = 'D'
            elif row['archive_reason'] == '0':
                row['archive_reason'] = 'E'

            nationalities = {'1': 'LY', '2': 'EG', '3': 'SD',
                             '4': 'IQ', '5': 'TN', '6': 'PS',
                             '7': 'JO', '8': 'LB', '9': 'YE',
                             '10': 'SY', '11': 'MA', '12': 'PK',
                             '13': 'TD', '14': 'TR', '16': 'IR',
                             '17': 'DZ', '18': 'NE', '19': 'ER',
                             '20': 'DJ', '21': 'MR'}

            row['nationality'] = nationalities.get(row['nationality'], 'LY')

            try:
                student = Student.objects.get(
                    registration_number=row['registration_number'],
                )
                if row['registration_number'] not in DUPLICATE_STUDENTS:
                    DUPLICATE_STUDENTS.append(row['registration_number'])

            except Student.DoesNotExist:
                student = Student.objects.create(
                    first_name=row['first_name'],
                    first_name_ar=row['first_name_ar'],
                    last_name=row['last_name'],
                    last_name_ar=row['last_name_ar'],
                    registration_number=row['registration_number'],
                    gender=row['gender'],
                    date_of_birth=row['date_of_birth'],
                    status=row['archive_reason'],
                    nationality=row['nationality']
                )
                if verbosity > 1:
                    print("Created student {}".format(
                        row['registration_number']
                    ))
            try:
                user = pXUser.objects.get(
                    email=(row['registration_number'] +
                           '@students.uot.edu.ly'))
            except pXUser.DoesNotExist:
                user = pXUser.objects.create_user(
                    email=(row['registration_number'] +
                           '@students.uot.edu.ly'),
                    password=row['registration_number'][::-1])
                UserProfile.objects.create(user=user, profile=student)
                if verbosity > 1:
                    print("Created user {}".format(
                        row['registration_number']
                    ))

    if len(DUPLICATE_STUDENTS) != 0:
        conflicts.write("\nThese students were found in both"
                        " the main DB and the archive DB, a very"
                        " stupid thing. I'll take the student record"
                        " stored in the archive DB:\n")

    i = 1
    for student in DUPLICATE_STUDENTS:
        conflicts.write(
            "{}- Student: {}\n"
            .format(i, student,))
        i += 1


def create_users(config):
    conflicts_file = (config['LOGS_FILES_LOCATION'] + '/' +
                      'STUDENT_CONFLICTS.txt')
    conflicts = open(conflicts_file, 'w')

    for file in config['FILES']:
        prepared_file = (
            config['PREPARED_FILES_LOCATION'] + '/' + 'students' +
            '_' + file[:-4] + '.csv'
        )
        students_table_process(
            prepared_file,
            config['FIELDS'][file].get('process_fields').get('STUDENTS'),
            conflicts,
            config['VERBOSITY'])

    conflicts.close()


def assign_advisors(config):

    files = ['advisors_NEWNEW.csv']
    for file in files:
        with open(config['MDE_FILE_LOCATION'] + '/cleaning/' + file, 'rb') as csvfile:
            reader = unicodecsv.DictReader(
                csvfile, fieldnames=['registration_number',
                                     'student_name', 'advisor'])
            for row in reader:
                registration_number_handler(row)
                if config['VERBOSITY'] > 1:
                        print("I'll now process {}, {}"
                              .format(row['registration_number'],
                                      row['student_name']))
                student = Student.objects.get(
                    registration_number=row['registration_number']
                )
                student.advisor = row['advisor']
                student.save()
