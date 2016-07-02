import unicodecsv
from general_handlers import period_handler
# from django.db import IntegrityError

from ....administration.models import Department
from ....administration.courses.models import (Course, PeriodCourse, Section)

from ....administration.periods.models import Period
# from ....users.models import pXUser, UserProfile, Employee
from ....students.models import Student
from ....students.section_enrolments.models import (SectionEnrolment,
                                                    SectionEnrolmentLog)
from ....students.period_registrations.models import PeriodRegistration
from ....administration.degrees.models import Degree, PeriodDegree
from ....administration.courses.assessments.models import (
    AssessmentResult, AssessmentType, Assessment)

import re

from ....administration.courses.signals import (
    disconnect_period_course_signals,
    connect_period_course_signals)
from ....students.section_enrolments.signals import (
    disconnect_section_enrolment_signals,
    connect_section_enrolment_signals)
from ....administration.courses.assessments.signals import (
    disconnect_asessement_signals,
    connect_assessment_signals,
    disconnect_assessment_type_signals,
    connect_assessment_type_signals,
    disconnect_assessment_result_signals,
    connect_assessment_result_signals
)

def registration_table_read(file, fieldnames, rows):
    with open(file, 'rb') as csvfile:
        reader = unicodecsv.DictReader(csvfile, fieldnames)
        for row in reader:
            period_handler(row)
            row.pop(None, None)
            row.pop('')
            rows.append(row)


def registration_table_write(file, fieldnames, rows):
    with open(file, 'w') as csvfile:
        writer = unicodecsv.DictWriter(csvfile, fieldnames)
        writer.writeheader()
        for row in rows:
            if row['registration_number'][0] != '0':
                row['registration_number'] = ('0' + row['registration_number'])
            if row['grade'] == '-1.0000000000000000e+00':
                row['grade'] = None
            writer.writerow(row)


def registration_table_process(file, fieldnames, conflicts, verbosity):
    disconnect_period_course_signals()
    disconnect_section_enrolment_signals()
    disconnect_asessement_signals()
    disconnect_assessment_type_signals()
    disconnect_assessment_result_signals()

    UNKNOWN_STUDENTS = {}
    REPEATED_ENROLMENTS = {}
    UNKNOWN_PERIODS = []
    UNKNOWN_REGISTRATIONS = {}
    DUPLICATE_REGISTRATIONS = {}
    NEW_COURSES = []

    with open(file, 'rb') as csvfile:
        reader = unicodecsv.DictReader(csvfile, fieldnames)
        next(reader, None)
        for row in reader:
            try:
                course = Course.objects.get(code=row['code'],
                                            credit=row['credit'])
            except Course.DoesNotExist:
                '''
                AE200 and AE325 were once 2 credits,
                so we need to create them manually,
                this should probably be placed in another place
                '''
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
                    level=int(re.search('\d+', row['code']).group()[0]) * 100,
                    notes="WHAT IS THIS?",
                    department=Department.objects.all()[0])
                NEW_COURSES.append(row['code'])

            try:
                student = Student.objects.get(
                    registration_number=row['registration_number'])
            except Student.DoesNotExist:
                if UNKNOWN_STUDENTS.get(row[
                        'registration_number']) is not None:
                    UNKNOWN_STUDENTS[row['registration_number']] += 1
                else:
                    UNKNOWN_STUDENTS[row['registration_number']] = 1
                continue

            try:
                period = Period.objects.get(period=row['period'],
                                            academic_year=row['academic_year'])
            except Period.DoesNotExist:
                period = Period.objects.create(
                    period=row['period'],
                    academic_year=row['academic_year'])
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
                period=period,
                course=course)
            if verbosity > 1:
                if msg:
                    print('Created course {} in period {}'
                          .format(course, period))
            total_assessment_type = AssessmentType.objects.get(
                assessment_type='Total')

            total_assessment, msg = period_course.assessments.get_or_create(
                        assessment_type=total_assessment_type,
                        total_grade=100)

            section, msg = Section.objects.get_or_create(
                period_course=period_course,
                group=row['group'])
            if verbosity > 1:
                if msg:
                    print('Created section {}'.format(section))

            if row['registration_type'] == '1':
                registration_type = 'NS'
            elif row['registration_type'] == '0':
                registration_type = 'R'
            try:
                period_registration = (
                    PeriodRegistration.objects.get(student=student,
                                                   period=period))
                if period_registration.registration_type != registration_type:
                    if DUPLICATE_REGISTRATIONS.get(row[
                            'registration_number']) is not None:
                        DUPLICATE_REGISTRATIONS[row[
                            'registration_number']].append(
                                {'period': period,
                                 'registration_type':
                                 period_registration.registration_type,
                                 'new_registration_type': registration_type})
                    else:
                        DUPLICATE_REGISTRATIONS[row['registration_number']] = [
                            {
                                'period': period,
                                'registration_type':
                                period_registration.registration_type,
                                'new_registration_type': registration_type
                            }
                        ]
                    if registration_type == 'NS':
                        period_registration.registration_type = registration_type
                        period_registration.save()
            except PeriodRegistration.DoesNotExist:
                period_registration = (PeriodRegistration.objects.create(
                    student=student,
                    period=period,
                    registration_type=registration_type))
                if UNKNOWN_REGISTRATIONS.get(row[
                        'registration_number']) is not None:
                    UNKNOWN_REGISTRATIONS[row['registration_number']].append(
                        {'period': period,
                         'registration_type':
                         period_registration.registration_type, })
                else:
                    UNKNOWN_REGISTRATIONS[row['registration_number']] = [{
                        'period': period,
                        'registration_type':
                        period_registration.registration_type,
                    }]

            if (row['added_or_dropped'] == 'A' or
                    row['added_or_dropped'] == 'D'):
                try:
                    section_enrolment_log = SectionEnrolmentLog.objects.get(
                        section=section,
                        period_registration=period_registration,
                        enrolment_status=row['added_or_dropped'])
                except SectionEnrolmentLog.DoesNotExist:
                    section_enrolment_log = SectionEnrolmentLog.objects.create(
                        section=section,
                        period_registration=period_registration,
                        enrolment_status=row['added_or_dropped'])

            if row['grade'] == '':
                row['grade'] = None

            row['grade'] = float(row['grade']) if row['grade'] is not None else None
            total_assessment.result_status = 'P'
            total_assessment.save()

            if (row['added_or_dropped'] != 'D' or row['status'] != '0'):
                try:
                    section_enrolment = SectionEnrolment.objects.get(
                        section=section,
                        period_registration=period_registration)
                    section_enrolment_total, msg = section_enrolment.assessment_results.get_or_create(
                        assessment=total_assessment)
                    # if (row['grade'] is not None and
                    #         section_enrolment_total._grade != row['grade']):

                    if REPEATED_ENROLMENTS.get(student.registration_number) is not None:
                        REPEATED_ENROLMENTS[
                            student.registration_number].append({
                                'section': section,
                                'period_registration': period_registration,
                                'grade': section_enrolment_total._grade,
                                'other_grade': row['grade']
                            })
                    else:
                        REPEATED_ENROLMENTS[
                            student.registration_number] = [{
                                'section': section,
                                'period_registration': period_registration,
                                'grade': section_enrolment.grade,
                                'other_grade': row['grade']
                            }]

                    if (section_enrolment_total._grade is None and
                        row['grade'] is not None):
                        section_enrolment_total._grade=row['grade']
                        section_enrolment_total.save()
                        # print(section_enrolment_total.grade)

                except SectionEnrolment.DoesNotExist:
                    section_enrolment = SectionEnrolment.objects.create(
                        section=section,
                        period_registration=period_registration)
                    section_enrolment_total, msg = section_enrolment.assessment_results.get_or_create(
                        assessment=total_assessment)
                    section_enrolment_total._grade=row['grade']
                    section_enrolment_total.save()

                    if verbosity > 1:
                        print('Created student enrolment {}'
                              .format(section_enrolment))

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
                            .format(conflict['section'], conflict['grade'],
                                    conflict['other_grade']))
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
            conflicts.write("Period: {}, Registration Type: {}\n".format(
                conflict['period'], conflict['registration_type']))
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
                            .format(conflict['period'], conflict[
                                'registration_type'], conflict[
                                    'new_registration_type']))
        i += 1

    if len(NEW_COURSES) != 0:
        conflicts.write("\nNew courses created, they were created due"
                        " to difference in credit.\n")
    i = 1
    for course in NEW_COURSES:
        conflicts.write("{}- Course: {}\n".format(i, course))
        i += 1

    # some cleaning up because I disabled signals:

    # because of disabling period_courses signals
    for period_course in PeriodCourse.objects.all():
        final_exam = AssessmentType.objects.get(
            assessment_type='Final Examination')
        course_work = AssessmentType.objects.get(
            assessment_type='Course Work')
        period_course.assessments.get_or_create(
            assessment_type=course_work,
            total_grade=40)
        period_course.assessments.get_or_create(
            assessment_type=final_exam,
            total_grade=60)

    # because of disabling section_enrolment signals
    for section_enrolment in SectionEnrolment.objects.all():
        for assessment in Assessment.objects.filter(
            period_course=section_enrolment.section.period_course):
            section_enrolment.assessment_results.get_or_create(
                assessment=assessment)

    AssessmentResult.objects.filter(
        grade=-1).update(grade=None)


    # because of disabling assessment_result signals
    for assessment_result in AssessmentResult.objects.filter(
        assessment__assessment_type__assessment_type='Total'):
        assessment_result.grade = assessment_result._grade
        assessment_result.save()
        section_enrolment = assessment_result.section_enrolment
        section_enrolment.grade = assessment_result.grade
        section_enrolment.save()

    # for non registered periods, delete all enrolments
    SectionEnrolment.objects.exclude(
        period_registration__registration_type='R').delete()


    # turn on the signals again
    connect_assessment_signals()
    connect_period_course_signals()
    connect_assessment_type_signals()
    connect_assessment_result_signals()
    connect_section_enrolment_signals()


def create_enrolments(config):
    conflicts_file = (config['LOGS_FILES_LOCATION'] + '/' +
                      'ENROLMENT_CONFLICTS.txt')
    conflicts = open(conflicts_file, 'w')

    for file in config['FILES']:
        prepared_file = (
            config['PREPARED_FILES_LOCATION'] + '/' + 'registration' +
            '_' + file[:-4] + '.csv'
        )
        registration_table_process(
            prepared_file,
            config['FIELDS'][file].get('process_fields').get('REGISTRATION'),
            conflicts,
            config['VERBOSITY'])

    conflicts.close()
