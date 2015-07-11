import unicodecsv
from general_handlers import period_handler
from django.db import IntegrityError

from UIS.models.administration import Department
from UIS.models.courses import (CourseCatalogue, PeriodCourse,
                                Section, SectionType, PeriodCourseSectionType)
from UIS.models.time_period import Period, PeriodDegree
from UIS.models.users import UISUser, UserProfile, Employee
from UIS.models.students import (Student, StudentEnrolment,
                                 StudentRegistration)
from UIS.models.degrees import Degree
import re


def registration_table_read(file, fieldnames, rows):
    with open(file, 'rb') as csvfile:
        reader = unicodecsv.DictReader(
            csvfile, fieldnames)
        for row in reader:
            period_handler(row)
            row.pop(None, None)
            row.pop('')
            rows.append(row)


def registration_table_write(file, fieldnames, rows):
    with open(file, 'w') as csvfile:
        writer = unicodecsv.DictWriter(
            csvfile, fieldnames)
        writer.writeheader()
        for row in rows:
            if row['registration_number'][0] != '0':
                row['registration_number'] = (
                    '0' + row['registration_number']
                )
            writer.writerow(row)


def registration_table_process(file, fieldnames, conflicts, verbosity):
    with open(file, 'rb') as csvfile:
        reader = unicodecsv.DictReader(
            csvfile, fieldnames)
        next(reader, None)
        for row in reader:
            try:
                course = CourseCatalogue.objects.get(
                    code=row['code'], credit=row['credit'])
            except CourseCatalogue.DoesNotExist:
                course = CourseCatalogue.objects.create(
                    code=row['code'],
                    credit=row['credit'],
                    name='UNKNOWN COURSE',
                    level=int(
                        re.search(
                            '\d+', row['code']
                        ).group()[0]
                    )*100,
                    notes="WHAT IS THIS?",
                    department=Department.objects.all()[0])
                conflicts.write("Created course {},"
                                "WHAT IS THIS!, it shouldn't"
                                "have been created\n"
                                .format(row['code']))
                if verbosity > 1:
                    print "Created course {}, WHAT IS THIS!".format(
                        row['code']
                    )

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
                    print "Created user {}, WHO IS THIS?".format(
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
            period_course, msg = PeriodCourse.objects.get_or_create(
                        period=period, course=course)
            if verbosity > 1:
                if msg:
                    print('Created course {} in period {}'
                          .format(course, period)
                    )
            section_type, msg = SectionType.objects.get_or_create(
                name='Main'
            )
            period_course_section_type, msg = PeriodCourseSectionType.objects.get_or_create(
                period_course=period_course,
                section_type=section_type
                )
            section, msg = Section.objects.get_or_create(
                section_type=period_course_section_type,
                group=row['group'])
            if verbosity > 2:
                if msg:
                    print('Created section {}'.format(section))

            if row['registration_type'] == '1':
                registration_type = 'NS'
            elif row['registration_type'] == '0':
                registration_type = 'R'
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
            
            if row['added_or_dropped'] == 'D' or row['status'] == '0':
                continue
            else:
                student_enrolment, msg = (
                    StudentEnrolment.objects.get_or_create(
                        section=section,
                        student_registration=student_registration,
                        grade=row['grade'],
                    )
                )
                if verbosity > 1:
                    if msg:
                        print('Created student enrolment {}'
                              .format(student_enrolment))
    StudentEnrolment.original.filter(grade=-1).update(grade=None)
