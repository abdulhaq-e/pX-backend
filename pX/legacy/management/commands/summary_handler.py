import unicodecsv

from django.db import IntegrityError

from general_handlers import (period_handler, registration_number_handler)

from ....students.models import Student
# from ....students.section_enrolments.models import SectionEnrolment
from ....students.period_registrations.models import PeriodRegistration

# from ....users.models import pXUser, UserProfile, Employee

from ....administration.periods.models import Period
from ....administration.degrees.models import Degree, PeriodDegree


def summary_table_read(file, fieldnames, rows):
    with open(file, 'rb') as csvfile:
        reader = unicodecsv.DictReader(
            csvfile, fieldnames)
        for row in reader:
            registration_number_handler(row)
            period_handler(row)
            row.pop(None, None)
            rows.append(row)


def summary_table_write(file, fieldnames, rows):

    with open(file, 'w') as csvfile:
        writer = unicodecsv.DictWriter(
            csvfile, fieldnames)
        writer.writeheader()
        for row in rows:
            period_handler(row)
            writer.writerow(row)


def summary_table_process(file, fieldnames, conflicts, verbosity):

    UNKNOWN_STUDENTS = {}
    DUPLICATE_REGISTRATIONS = {}

    with open(file, 'rb') as csvfile:
        reader = unicodecsv.DictReader(
            csvfile, fieldnames
        )
        next(reader, None)
        for row in reader:
            if row['registration_type'] == '':
                registration_type = 'R'
            elif row['registration_type'] == 'S':
                registration_type = 'NS'
            elif row['registration_type'] == 'B':
                registration_type = 'D'

            try:
                student = Student.objects.get(
                    registration_number=row['registration_number'])
            except Student.DoesNotExist:
                if UNKNOWN_STUDENTS.get(row['registration_number']) is not None:
                    UNKNOWN_STUDENTS[row['registration_number']] += 1
                else:
                    UNKNOWN_STUDENTS[row['registration_number']] = 1
                continue

                # student = Student.objects.create(
                #     first_name='UNKNOWN STUDENT',
                #     first_name_ar='UNKNOWN STUDENT',
                #     last_name='UNKNOWN STUDENT',
                #     last_name_ar='UNKNOWN STUDENT',
                #     registration_number=row['registration_number'])
                # conflicts.write("Created student {},"
                #                 "WHO IS THIS!, student shouldn't"
                #                 "have been created. Found in 'summary' table\n"
                #                 .format(row['registration_number']))
                # if verbosity > 1:
                #     print "Created student {}, WHO IS THIS?".format(
                #         row['registration_number']
                #     )
                #     user, user_msg = UISUser.objects.get_or_create_user(
                #         email=(row['registration_number'] +
                #                '@students.uot.edu.ly'),
                #         password=row['registration_number'][::-1])
                #     if user_msg:
                #         UserProfile.objects.create(user=user, profile=student)

            period, msg = Period.objects.get_or_create(
                period=row['period'],
                academic_year=row['academic_year']
            )
            if verbosity > 1:
                if msg:
                    print('Created period {}.'
                          .format(period)
                    )
            period_degree, msg = PeriodDegree.objects.get_or_create(
                period=period,
                degree=Degree.objects.filter()[0])
            if verbosity > 1:
                if msg:
                    print('Created degree {} in period {}'
                          .format(Degree.objects.filter()[0], period)
                    )
            try:
                student_registration = (
                    PeriodRegistration.objects.get(
                        student=student,
                        period=period))
                if student_registration.registration_type != registration_type:
                    if DUPLICATE_REGISTRATIONS.get(row['registration_number']) is not None:
                        DUPLICATE_REGISTRATIONS[row['registration_number']].append(
                            {'period': period_degree.period,
                             'registration_type': student_registration.registration_type,
                             'new_registration_type': registration_type
                            })
                    else:
                        DUPLICATE_REGISTRATIONS[row['registration_number']] = [{
                            'period': period_degree.period,
                            'registration_type': student_registration.registration_type,
                            'new_registration_type': registration_type

                        }]
                    student_registration.registration_type = registration_type
                    student_registration.save()
            except PeriodRegistration.DoesNotExist:
                student_registration = (
                    PeriodRegistration.objects.create(
                        student=student,
                        period=period,
                        registration_type=registration_type))
                if verbosity > 1:
                    print('Created registration for student {} in period {}'
                          .format(student, period)
                    )

    conflicts.write("\nConflicts found in {}\n".format(file))

    if len(UNKNOWN_STUDENTS) != 0:
        conflicts.write("IGNORED STUDENTS (They are probably "
                        "the same as the ones reported in the "
                        "registration conflict file):\n")
    i = 1
    for student, enrolments in UNKNOWN_STUDENTS.iteritems():
        conflicts.write("{}- I have ignored {} registrations "
                        "for student {} because he/she is unknown.\n"
                        .format(i, enrolments, student))
        i += 1

    if len(DUPLICATE_REGISTRATIONS) != 0:
        conflicts.write("\nA stupid conflict, some of which maybe already"
                        " reported in the registration "
                        "conflict file, I have used the 'new registration"
                        " type'.\n")

    i = 1
    for student, CONFLICTS in DUPLICATE_REGISTRATIONS.iteritems():
        conflicts.write("{}- Student: {}\n".format(i, student))
        for conflict in CONFLICTS:
            conflicts.write("Period: {}, Original Registration Type: {}, "
                            "New Registration Type: {}\n"
                            .format(conflict['period'],
                                    conflict['registration_type'],
                                    conflict['new_registration_type']
                            ))
        i += 1
