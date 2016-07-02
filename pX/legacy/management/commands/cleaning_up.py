# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import unicodecsv

from django.db.models import Q
from ....students.models import Student
from ....students.section_enrolments.models import (SectionEnrolment,
                                                    SectionEnrolmentLog)
from ....students.period_registrations.models import PeriodRegistration
from ....administration.courses.models import Course

from .general_handlers import registration_number_handler

BASE = '../pX-tools/legacyDB/'


def exclusions():

    STUDENTS_EXCLUSIONS_MAIN = []
    STUDENTS_EXCLUSIONS_ARCHIVE = []
    STUDENTS_DUPLICATES = []

    exclusions = {
        'Register.mde': dict(
            [
                ('STUDENTS', STUDENTS_EXCLUSIONS_MAIN)
            ]
        ),
        'DBArchive.MDE': dict(
            [
                ('STUDENTS', STUDENTS_EXCLUSIONS_ARCHIVE)
            ]
        ),
        'DUPLICATES': dict(
            [
                ('STUDENTS', STUDENTS_DUPLICATES)
            ]
        )
    }

    return exclusions


def get_results():

    for i in Student.objects.all():
        i.get_results()


def clean_up_transferred(conflict, simulate):

    with open(BASE + 'cleaning/TRANSFERRED.csv', 'r') as transferred:
        reader = unicodecsv.DictReader(
            transferred, ['registration_number', 'name']
        )

        conflict.write("\nI will change the status of the following student"
                       " to transferred, this may not be accurate!!:\n")

        for i, row in enumerate(reader):
            conflict.write(
                "{}- Student: {}, {}\n"
                .format(i, row['registration_number'],
                        row['name']))
            registration_number_handler(row)
            if not simulate:
                student = Student.objects.filter(
                    registration_number=row['registration_number'])
                if student.exists():
                    s = student[0]
                    s.status = 'T'
                    s.save()


def clean_up_left(conflict, simulate):

    with open(BASE + 'cleaning/LEFT.csv', 'r') as transferred:
        reader = unicodecsv.DictReader(
            transferred, ['registration_number', 'name']
        )

        conflict.write("\nI will change the status of the following student"
                       " to left out, this may not be accurate!!:\n")

        for i, row in enumerate(reader):
            conflict.write(
                "{}- Student: {}, {}\n"
                .format(i, row['registration_number'],
                        row['name']))
            registration_number_handler(row)
            if not simulate:
                student = Student.objects.filter(
                    registration_number=row['registration_number'])
                if student.exists():
                    s = student[0]
                    s.status = 'L'
                    s.save()


def clean_up_graduates(conflict, simulate):

    with open(BASE + 'cleaning/GRADUATES.csv', 'r') as transferred:
        reader = unicodecsv.DictReader(
            transferred, ['registration_number', 'name']
        )

        conflict.write("\nI will change the status of the following student"
                       " to graduates, this may not be accurate!!:\n")

        for i, row in enumerate(reader):
            conflict.write(
                "{}- Student: {}, {}\n"
                .format(i, row['registration_number'],
                        row['name']))
            registration_number_handler(row)
            if not simulate:
                student = Student.objects.filter(
                    registration_number=row['registration_number'])
                if student.exists():
                    s = student[0]
                    s.status = 'G'
                    s.save()


def clean_up_delete_students(conflict, simulate):

    with open(BASE + 'cleaning/DELETE.csv', 'r') as transferred:
        reader = unicodecsv.DictReader(
            transferred, ['registration_number', 'name']
        )

        conflict.write("\nI will delete the following students"
                       " because they are not registered for any periods:\n")

        for i, row in enumerate(reader):
            conflict.write(
                "{}- Student: {}, {}\n"
                .format(i, row['registration_number'],
                        row['name']))
            registration_number_handler(row)
            if not simulate:
                student = Student.objects.filter(
                    registration_number=row['registration_number'])
                if student.exists():
                    # student.delete()
                    student_number = row['registration_number']
                    SectionEnrolment.objects.filter(
                        period_registration__student__registration_number=student_number
                    ).delete()
                    SectionEnrolmentLog.objects.filter(
                        period_registration__student__registration_number=student_number
                    ).delete()
                    PeriodRegistration.objects.filter(
                        student__registration_number=student_number).delete()
                    for j in Student.objects.filter(registration_number=student_number):
                        j.delete()


    DELETED_STUDENTS = {
        '02195315': {'name': "هالة ابوبكر عمارالجعيدي",
                     'reason': "This student does not belong to this department"}
    }

    conflict.write("\nI will delete the following students"
                   " for the reasons indicated :\n")
    i = 1
    for student_number, student in DELETED_STUDENTS.iteritems():
        conflict.write("{}- Student: {}, {}. Reason: {}\n"
                       .format(i, student_number,
                               student['name'], student['reason']))
        SectionEnrolment.objects.filter(
            period_registration__student__registration_number=student_number
        ).delete()
        SectionEnrolmentLog.objects.filter(
            period_registration__student__registration_number=student_number
        ).delete()
        PeriodRegistration.objects.filter(
            student__registration_number=student_number).delete()
        for j in Student.objects.filter(registration_number=student_number):
            j.delete()
        i += 1


def correct_gender(conflict):

    GENDER = {
        "02101338": "M",
        "02202123": "F",
        "02201645": "M"
    }

    conflict.write('\nFound students with empty gender field'
                   ', fixed everything:\n')
    i = 1
    for student, gender in GENDER.iteritems():
        a = Student.objects.get(registration_number=student)
        a.gender = gender
        a.save()
        conflict.write("{}- Student: {}, {}\n"
                       .format(i, student, a))
        i += 1


def clean_up_dropped_out_students(conflict, simulate):

    with open(BASE + 'cleaning/DROPPED_OUT.csv', 'r') as dropped:
        reader = unicodecsv.DictReader(
            dropped, ['registration_number', 'name', 'last',
                      'reg', 'pass']
        )

        conflict.write("\nI will change the status of the following student"
                       " to dropped out, this is based on the fact that"
                       " they're not graduates and didn't register for any"
                       " of the previous 4 semesters.\nI have listed along"
                       " with the number and name, their last registration"
                       " and the CUMULATIVE REGISTERED CREDITS and "
                       " CUMULATIVE PASSED CREDITS:\n")

        for i, row in enumerate(reader):
            conflict.write(
                "{}- Student: {}, {}, {}, {}, {}\n"
                .format(i, row['registration_number'],
                        row['name'],
                        row['last'],
                        row['reg'],
                        row['pass']))
            registration_number_handler(row)
            if not simulate:
                student = Student.objects.filter(
                    registration_number=row['registration_number'])
                if student.exists():
                    s = student[0]
                    s.status = 'D'
                    s.save()


def clean_up_course_names():

    courses = Course.objects.filter(
        Q(name__endswith='Ii') |
        Q(name__endswith='Iii') |
        Q(name__endswith='Iv') |
        Q(name__endswith='Vi')
    )
    for course in courses:
        split = course.name.split()
        split[-1] = split[-1].upper()
        course.name = ' '.join(split)
        course.save()

    course = Course.objects.get(code='GS112L')
    course.name = "Physics Lab"
    course.save()


def clean_up_equalled_courses():

    courses = {
        'GE133': ['AE133', 'CE133'],
        'GS101': ['GS103', ],
        'GS102': ['GS103', ],
        'GS203': ['GS104', ],
        'GS204': ['GS104', ],
        'GS111': ['GS113', ],
        'GS112': ['GS113', ],
        'GS112L': ['GS113L', ],
        'GH141': ['GH140N', ],
        'GH142': ['GH140N', ],
        'EE280': ['EE200', ],
        'GE222': ['GE123', ],
        'GS200': ['EC251', 'GE108'],
        'AE210': ['ME210', ],
        'GE121': ['GE122N', 'GE124E'],
        'GE222': ['GE123', 'GE124E'],
    }

    for key, val in courses.items():
        course = Course.objects.get(code=key)
        for i in val:
            equalled = Course.objects.get(code=i)
            course.equalled_courses.add(equalled)
