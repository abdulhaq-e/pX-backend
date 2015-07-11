import unicodecsv

from django.db import IntegrityError

from general_handlers import (period_handler, registration_number_handler)

from UIS.models.students import (Student, StudentEnrolment,
                                 StudentRegistration)
from UIS.models.users import UISUser, UserProfile, Employee
from UIS.models.time_period import Period, PeriodDegree

from UIS.models.degrees import Degree


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
                student = Student.objects.create(
                    first_name='UNKNOWN STUDENT',
                    first_name_ar='UNKNOWN STUDENT',
                    last_name='UNKNOWN STUDENT',
                    last_name_ar='UNKNOWN STUDENT',
                    registration_number=row['registration_number'])
                conflicts.write("Created student {},"
                                "WHO IS THIS!, student shouldn't"
                                "have been created\n"
                                .format(row['registration_number']))
                if verbosity > 1:
                    print "Created student {}, WHO IS THIS?".format(
                        row['registration_number']
                    )
                    user, user_msg = UISUser.objects.get_or_create_user(
                        email=(row['registration_number'] +
                               '@students.uot.edu.ly'),
                        password=row['registration_number'][::-1])
                    if user_msg:
                        UserProfile.objects.create(user=user, profile=student)

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
                student_registration, msg = (
                    StudentRegistration.objects.get_or_create(
                        student=student,
                        period_degree=period_degree,
                        registration_type=registration_type)

                )
            except IntegrityError:
                conflicts.write(
                    "STUDENT {} has a SERIOUS conflict."
                    "Probably two registrations" 
                    "with different status\n"
                    .format(row['registration_number']))
                continue
