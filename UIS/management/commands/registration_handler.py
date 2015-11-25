import unicodecsv
from general_handlers import period_handler
from django.db import IntegrityError

from UIS.models.administration import Department
from UIS.models.courses import (Course, PeriodCourse,
                                Section, SectionType, PeriodCourseSectionType)
from UIS.models.time_period import Period, PeriodDegree
from UIS.models.users import UISUser, UserProfile, Employee
from UIS.models.students import (Student, StudentEnrolment,
                                 StudentRegistration, StudentEnrolmentLog)
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
            if row['grade'] == '-1.0000000000000000e+00':
                row['grade'] = None
            writer.writerow(row)


def registration_table_process(file, fieldnames, conflicts, verbosity):

    UNKNOWN_STUDENTS = {}
    REPEATED_ENROLMENTS = {}
    UNKNOWN_PERIODS = []
    UNKNOWN_REGISTRATIONS = {}
    DUPLICATE_REGISTRATIONS = {}
    NEW_COURSES = []

    with open(file, 'rb') as csvfile:
        reader = unicodecsv.DictReader(
            csvfile, fieldnames)
        next(reader, None)
        for row in reader:
            try:
                course = Course.objects.get(
                    code=row['code'], credit=row['credit'])
            except Course.DoesNotExist:
                if row['code'] == 'AE200':
                    name = 'Introduction To Aeronautics'
                elif row['code'] == 'AE325':
                    name = 'Introduction To Numerical'
                else:
                    name = 'UNKOWN COURSE'

                course = Course.objects.create(
                    code=row['code'],
                    credit=row['credit'],
                    name=name,
                    level=int(
                        re.search(
                            '\d+', row['code']
                        ).group()[0]
                    )*100,
                    notes="WHAT IS THIS?",
                    department=Department.objects.all()[0])
                NEW_COURSES.append(row['code'])

            try:
                student = Student.objects.get(
                    registration_number=row['registration_number'])
            except Student.DoesNotExist:
                if UNKNOWN_STUDENTS.get(row['registration_number']) is not None:
                    UNKNOWN_STUDENTS[row['registration_number']] += 1
                else:
                    UNKNOWN_STUDENTS[row['registration_number']] = 1
                continue

            try:
                period = Period.objects.get(
                    period=row['period'],
                    academic_year=row['academic_year']
                )
            except Period.DoesNotExist:
                period = Period.objects.create(
                    period=row['period'],
                    academic_year=row['academic_year']
                )
                if str(period) not in UNKNOWN_PERIODS:
                    UNKNOWN_PERIODS.append(str(period))


            try:
                period_degree = PeriodDegree.objects.get(
                    period=period,
                    degree=Degree.objects.filter()[0])
            except PeriodDegree.DoesNotExist:
                period_degree = PeriodDegree.objects.create(
                    period=period,
                    degree=Degree.objects.filter()[0])
                conflicts.write("Created a period degree which is weird.\n")

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
                student_registration = (
                    StudentRegistration.objects.get(
                        student=student,
                        period_degree=period_degree))
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
                    if registration_type == 'NS':
                        student_registration.registration_type = registration_type
                        student_registration.save()
            except StudentRegistration.DoesNotExist:
                student_registration = (
                    StudentRegistration.objects.create(
                        student=student,
                        period_degree=period_degree,
                        registration_type=registration_type))
                if UNKNOWN_REGISTRATIONS.get(row['registration_number']) is not None:
                    UNKNOWN_REGISTRATIONS[row['registration_number']].append(
                        {'period': period_degree.period,
                         'registration_type': student_registration.registration_type,
                        })
                else:
                    UNKNOWN_REGISTRATIONS[row['registration_number']] = [{
                        'period': period_degree.period,
                        'registration_type': student_registration.registration_type,
                    }]

            if (row['added_or_dropped'] == 'A' or
                row['added_or_dropped'] == 'D'):
                try:
                    student_enrolment_log = StudentEnrolmentLog.objects.get(
                        section=section,
                        student_registration=student_registration,
                        enrolment_status=row['added_or_dropped'])
                except StudentEnrolmentLog.DoesNotExist:
                    student_enrolment_log = StudentEnrolmentLog.objects.create(
                        section=section,
                        student_registration=student_registration,
                        enrolment_status=row['added_or_dropped'])

            if row['grade'] == '':
                row['grade'] = None
            if (row['added_or_dropped'] != 'D' or row['status'] != '0'):
                try:
                    student_enrolment = StudentEnrolment.objects.get(
                        section=section,
                        student_registration=student_registration)

                    if (row['grade'] is not None and
                        student_enrolment.grade != float(row['grade'])):


                        if REPEATED_ENROLMENTS.get(student) is not None:
                            REPEATED_ENROLMENTS[student.registration_number].append(
                                {
                                    'section': section,
                                    'student_registration': student_registration,
                                    'grade': student_enrolment.grade,
                                    'other_grade': row['grade']
                                })
                        else:
                            REPEATED_ENROLMENTS[student.registration_number] = [{
                                'section': section,
                                'student_registration': student_registration,
                                'grade': student_enrolment.grade,
                                'other_grade': row['grade']
                            }]

                        if student_enrolment.grade is None:
                            student_enrolment.grade = row['grade']
                            student_enrolment.save()

                except StudentEnrolment.DoesNotExist:
                    student_enrolment = StudentEnrolment.objects.create(
                            section=section,
                            student_registration=student_registration,
                            grade=row['grade'])
                    if verbosity > 1:
                        print('Created student enrolment {}'
                              .format(student_enrolment))

    conflicts.write("\nConflicts found in {}\n".format(file))

    if len(UNKNOWN_STUDENTS) != 0:
        conflicts.write("IGNORED STUDENTS (They are probably "
                        "the same as the ones reported in the "
                        "registration conflict file):\n")
    i = 1
    for student, enrolments in UNKNOWN_STUDENTS.iteritems():
        conflicts.write("{}- I have ignored {} enrolments "
                        "for student {} because he/she is unknown.\n"
                        .format(i, enrolments, student))
        i += 1

    if len(REPEATED_ENROLMENTS) != 0:
        conflicts.write("\nSHOCKING CONFLICT..., REPEATED ENROLMENTS"
                        " WITH DIFFERENT GRADES, for Non-Empty Grade"
                        " vs Empty Grade, I have chosen the Non-Empty"
                        " Grade, for anything else, I chose whatever"
                        " appeared first. The latter situation is very"
                        " fishy and requires investigation!:\n")
    i = 1
    for student, CONFLICTS in REPEATED_ENROLMENTS.iteritems():
        conflicts.write("{}- Student: {}\n".format(i, student))
        for conflict in CONFLICTS:
            conflicts.write("Section: {}, Original Grade: {}, "
                            "New Grade: {}\n"
                            .format(conflict['section'],
                                    conflict['grade'],
                                    conflict['other_grade']
                            ))
        i += 1

    if len(UNKNOWN_PERIODS) != 0:
        conflicts.write("\nStupid Conflict, new periods which shouldn't"
                        " have been created:\n")
    i = 1
    for period in UNKNOWN_PERIODS:
        conflicts.write("{}- Period: {}.\n".format(i, period))
        i += 1

    if len(UNKNOWN_REGISTRATIONS) != 0:
        conflicts.write("\nA very stupid conflict too, "
                        "found new registrations which is very weird.\n")

    i = 1
    for student, CONFLICTS in UNKNOWN_REGISTRATIONS.iteritems():
        conflicts.write("{}- Student: {}\n".format(i, student))
        for conflict in CONFLICTS:
            conflicts.write("Period: {}, Registration Type: {}\n"
                            .format(conflict['period'],
                                    conflict['registration_type']
                            ))
        i += 1

    if len(DUPLICATE_REGISTRATIONS) != 0:
        conflicts.write("\nA stupid conflict, some of which maybe already"
                        " reported in the registration "
                        "conflict file, I chose 'NS'.\n")

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

    if len(NEW_COURSES) != 0:
        conflicts.write("\nNew courses created, they were created due"
                        " to difference in credit.\n")
    i = 1
    for course in NEW_COURSES:
        conflicts.write("{}- Course: {}\n"
                        .format(i, course))
        i += 1

    StudentEnrolment.original.filter(grade=-1).update(grade=None)
    StudentEnrolment.objects.exclude(
        student_registration__registration_type='R').delete()
