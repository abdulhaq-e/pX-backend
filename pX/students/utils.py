# -*- coding: utf-8 -*-
from __future__ import division, unicode_literals

import os
from subprocess import Popen, PIPE

from django.db.models import Q
from django.template.loader import get_template

from .section_enrolments.models import SectionEnrolment
from ..administration.courses.models import (Course, CoursePrerequisite)
from ..administration.periods.models import Period
from .temp_models import StudentAllowedEnrolment
from .temp_models import StudentResult


def _update_results(period_registration, data):
    return StudentResult.objects.create(
        period_registration=period_registration, **data)


def calculate_results(student):
    """
    needs to be documented!
    """

    # StudentResult.objects.filter(
    # period_registration__student=student).delete()
    all_enrolments = SectionEnrolment.custom.filter(
        period_registration__student=student).enroled()
    enrolments = all_enrolments.filter(
        period_registration__registration_type='R'
    )
    # the above two should be the same (i think)
    period_registrations = student.period_registrations.all()

    period_count = 0
    actual_period_count = period_count
    j = 0

    for i in period_registrations:
        if (not all_enrolments.filter(
                period_registration=i).exists() and
            i.registration_type not in ['DS', 'ES', 'NS']):
            i.registration_type = 'D'
            i.save()

        period_count += 1
        if i.registration_type in ['DS', 'ES', 'NS']:
            pass
        # actual_period_count += 0
        else:
            actual_period_count += 1

        data = dict(
            [('period_count', period_count),
             ('actual_period_count', actual_period_count)
             ]
        )

        if j == 0:
            if i.registration_type == 'R':
                period_enrolments = enrolments.filter(
                    period_registration=i
                )
                repeated_enrolments = enrolments.none()
                data.update(
                    period_enrolments.get_statistics(
                        credits='registered_credits',
                        points='scored_points').items() +
                    period_enrolments.passed().get_statistics(
                        credits='passed_credits',
                        points='passed_points').items() +
                    repeated_enrolments.get_statistics(
                        credits='repeated_credits',
                        points='repeated_points').items()
                )
                try:
                    data.update({
                        'GPA':
                        round(data['scored_points'] /
                              data['registered_credits'], 2)
                    })
                except ZeroDivisionError:
                    data.update({
                        'GPA': 0.0
                    })
                data.update({
                    'cumulative_scored_points':
                    data['scored_points'],
                    'cumulative_registered_credits':
                    data['registered_credits'],
                    'cumulative_passed_credits':
                    data['passed_credits'],
                    'previous_GPA': 0.0
                })
                try:
                    data.update({
                        'cumulative_GPA':
                        round(data['cumulative_scored_points'] /
                              data['cumulative_registered_credits'], 2)
                    })
                except ZeroDivisionError:
                    data.update({
                        'cumulative_GPA': 0.0
                    })

                if data['cumulative_GPA'] < 50:
                    data.update({
                        'warnings': 1,
                        'previous_warnings': 0,
                    })
                else:
                    data.update({
                        'warnings': 0,
                        'previous_warnings': 0,
                    })
                if data['cumulative_GPA'] < 35:
                    data.update({
                        'very_poor_warnings': 1,
                    })
                else:
                    data.update({
                        'very_poor_warnings': 0,
                    })

                _update_results(i, data)
            elif i.registration_type in ['D', 'DS', 'ES', 'NS']:
                data.update({
                    'registered_credits': 0.0,
                    'scored_points': 0.0,
                    'passed_credits': 0.0,
                    'passed_points': 0.0,
                    'repeated_credits': 0.0,
                    'repeated_points': 0.0,
                    'GPA': 0.0,
                    'cumulative_scored_points': 0.0,
                    'cumulative_registered_credits': 0.0,
                    'cumulative_passed_credits': 0.0,
                    'cumulative_GPA': 0.0,
                    'previous_GPA': 0.0,
                    'warnings': 0,
                    'previous_warnings': 0,
                    'very_poor_warnings': 0,
                })
                _update_results(i, data)
        elif j != 0:
            if i.registration_type in ['D', 'DS', 'ES', 'NS']:
                previous_result = StudentResult.objects.get(
                    period_registration=period_registrations[j-1])

                data.update({
                    'registered_credits': 0.0,
                    'scored_points': 0.0,
                    'passed_credits': 0.0,
                    'passed_points': 0.0,
                    'repeated_credits': 0.0,
                    'repeated_points': 0.0,
                    'GPA': 0.0,
                    'cumulative_scored_points': previous_result.cumulative_scored_points,
                    'cumulative_registered_credits': previous_result.cumulative_registered_credits,
                    'cumulative_passed_credits': previous_result.cumulative_passed_credits,
                    'cumulative_GPA': previous_result.cumulative_GPA,
                    'previous_GPA': previous_result.cumulative_GPA,
                    'warnings': previous_result.warnings,
                    'previous_warnings': previous_result.warnings,
                    'very_poor_warnings': previous_result.very_poor_warnings,
                })
                _update_results(i, data)

                # except IntegrityError:

                #     # data.update({
                #     #     'period_registration': i}
                #     print 'hah'
                #     student.__update_results(i, data)
            elif i.registration_type == 'R':
                period_enrolments = enrolments.filter(
                    period_registration=i
                )
                equalled_with = []
                for z in period_enrolments:
                    equalled_with_temp = (
                        z.section.period_course.
                        course.equalled_with.all())
                    if equalled_with_temp.exists():
                        for equalled in equalled_with_temp:
                            equalled_with.append(equalled.code)
                repeated_enrolments_distinct = enrolments.failed().filter(
                    Q(code__in=period_enrolments.values_list(
                        'code', flat=True)) | Q(code__in=equalled_with)
                ).filter(
                    period_registration__in=[x for x in period_registrations[:j]]
                ).order_by(
                    'section__period_course__course__code',
                    '-section__period_course__period'
                ).distinct('section__period_course__course__code')

                repeated_enrolments = SectionEnrolment.custom.filter(
                    pk__in=repeated_enrolments_distinct.values_list(
                        'pk', flat=True))
                # results[j]['Enrolments'] = period_enrolments
                # results[j]['Repeated Enrolments'] = repeated_enrolments

                previous_result = StudentResult.objects.get(
                    period_registration=period_registrations[j-1])

                data.update(
                    period_enrolments.get_statistics(
                        credits='registered_credits',
                        points='scored_points').items() +
                    period_enrolments.passed().get_statistics(
                        credits='passed_credits',
                        points='passed_points').items() +
                    repeated_enrolments.get_statistics(
                        credits='repeated_credits',
                        points='repeated_points').items()
                )
                try:
                    data.update({
                        'GPA':
                        round(data['scored_points'] /
                              data['registered_credits'], 2)
                    })
                except ZeroDivisionError:
                    data.update({
                        'GPA': 0.0
                    })
                data.update({
                    'cumulative_scored_points': data['scored_points'] +
                    previous_result.cumulative_scored_points -
                    data['repeated_points'],
                    'cumulative_registered_credits':
                    data['registered_credits'] +
                    previous_result.cumulative_registered_credits -
                    data['repeated_credits'],
                    'cumulative_passed_credits':
                    data['passed_credits'] +
                    previous_result.cumulative_passed_credits,
                    'previous_GPA': previous_result.cumulative_GPA
                })
                try:
                    data.update({
                        'cumulative_GPA':
                        round(data['cumulative_scored_points'] /
                              data['cumulative_registered_credits'], 2)
                    })
                except ZeroDivisionError:
                    data.update({
                        'cumulative_GPA': 0.0
                    })

                if data['cumulative_GPA'] < 50:
                    data.update({
                        'previous_warnings': previous_result.warnings,
                        'warnings': previous_result.warnings + 1
                    })
                else:
                    data.update({
                        'previous_warnings': previous_result.warnings,
                        'warnings': 0
                    })

                if data['cumulative_GPA'] < 35:
                    data.update({
                        'very_poor_warnings': 1,
                    })
                else:
                    data.update({
                        'very_poor_warnings': 0,
                    })

                if (data['very_poor_warnings'] >= 2 or
                        data['warnings'] >= 3):
                        data.update({
                            'expulsion': True
                            })

                _update_results(i, data)

        j += 1


def get_allowed_enrolments(student):

    # Delete everything first
    student.allowed_enrolment.all().delete()

    # The first filter is excluding the passed courses.
    # first_filter = Course.objects.exclude(pk=student.get_passed_courses())

    # autumn 2011 filter needs to be done properly
    autumn2011 = Period.objects.get(academic_year='2011,2012', period=1)
    post_autumn2011 = Period.objects.filter(
        period__gte=autumn2011.period,
        academic_year__gte=autumn2011.academic_year)

    if (
        student.period_registrations.first().period not in
        post_autumn2011
    ):
        remaining_courses = student.get_remaining_courses().exclude(
            code='GS206')
    else:
        remaining_courses = student.get_remaining_courses()

    # fours years high school and mawada jouma'a
    four_years_high_school = ['022855391', '022804126', '022071317',
                              '021714174', '021714386', '02106341',
                              '022855128']
    if student.registration_number in four_years_high_school:
        remaining_courses = remaining_courses.exclude(
            code__in=['GE127', 'GS115', 'GS115L', 'ME201', 'ME307'])

    if student.registration_number == '021120007':
        remaining_courses = remaining_courses.exclude(
            code__in=['GE125', 'GE127', 'GE129', 'GH141',
                      'GH150', 'GS101', 'GS115', 'GS111'])

    prerequisites_restriction = (
        CoursePrerequisite.objects.filter(
            course__in=remaining_courses
            ).exclude(
                prerequisite__code__in=student.get_passed_courses().values_list(
                    'code', flat=True)
            ).exclude(
                prerequisite__equalled_courses__code__in=student.get_passed_courses().values_list(
                    'code', flat=True)
            )
        )

    allowed_enrolments = remaining_courses.exclude(
        prerequisites__in=prerequisites_restriction)

    general_courses = ['GS101', 'GS102', 'GS203', 'GS204',
                       'GS111', 'GS112', 'GS115', 'GS115L',
                       'GS200', 'GS206', 'GE121', 'GE125',
                       'GE127', 'GE129', 'GE133', 'GE222',
                       'GH141', 'GH142', 'GH150', 'GH151', ]
                       # LABS and GH152 have been omitted

    passed_120_credits = (student.period_registrations.last().
    student_result.cumulative_passed_credits < 120)

    passed_general_courses = remaining_courses.filter(
        code__in=general_courses
        ).exists()

    if not passed_120_credits or not passed_general_courses:
        allowed_enrolments = allowed_enrolments.exclude(code='AE599')

    excluded_from_regulations = ['GH152', 'GS112L',
                                 'GS115L', 'GE129L',
                                 'ME201', 'ME206',
                                 'ME215']
    elective = True

    level_100_exists = remaining_courses.exclude(
        code__in=excluded_from_regulations
        ).filter(
            level=100
            ).exists()
    if level_100_exists:
        allowed_enrolments = allowed_enrolments.exclude(
            level__in=[300, 400, 500])

        elective = False

    level_200_exists = remaining_courses.exclude(
        code__in=excluded_from_regulations
        ).filter(
            level=200
            ).exists()
    if level_200_exists:
        allowed_enrolments = allowed_enrolments.exclude(
            level__in=[400, 500])
        elective = False

    level_300_exists = remaining_courses.exclude(
        code__in=excluded_from_regulations
        ).filter(
            level=300
            ).exists()
    if level_300_exists:
        allowed_enrolments = allowed_enrolments.exclude(level=500)
        elective = False

    electives_finished = (student.get_passed_courses().values_list(
        'code', flat=True).filter(code__startswith='AE555').count()
        >= 6)

    if electives_finished:
        elective = False

    if elective:
        electives = Course.objects.filter(
            code__in=['AE555ADS', 'AE555EPM', 'AE555INS', 'AE555SMS',
                      'AE555AL']
            )
        exclusion = []
        passed_courses = student.get_passed_courses().values_list(
            'code', flat=True)
        if 'AE380' not in passed_courses:
            exclusion.append('AE555INS')
        if 'AE450' not in passed_courses:
            exclusion.append('AE555SMS')
        if 'AE412' not in passed_courses:
            exclusion.append('AE555ADS')

        possible_electives = electives.exclude(
            code__in=[student.get_passed_courses().values_list(
                'code', flat=True), exclusion])

        for c in possible_electives:
            StudentAllowedEnrolment.objects.create(
                student=student,
                course=c
                )
            # student.allowed_enrolment.add(electives)

    for c in allowed_enrolments:
        StudentAllowedEnrolment.objects.create(
            student=student,
            course=c
            )

        # student.allowed_enrolment.add(allowed_enrolments)

    return Course.objects.filter(
        studentallowedenrolment__in=student.allowed_enrolment.all()
        )

def get_passed_courses(student):
    return SectionEnrolment.custom.filter(
        period_registration__student=student).passed()



def get_max_allowed_credits(student):
    return (
        21 if student.period_registrations.last().
        student_result.cumulative_GPA > 75 else 18
    )


def get_failed_courses(student):
    return SectionEnrolment.custom.filter(
        period_registration__student=student).failed()


def get_enroled_courses(student):
    return SectionEnrolment.custom.filter(
        period_registration__student=student).enroled()


def get_remaining_courses(student):
    return (
        student.get_degree().courses.all().
            exclude(
                code__in=student.get_passed_courses().values_list(
                    'code', flat=True)).
            exclude(
                equalled_courses__code__in=student.get_passed_courses().
                values_list(
                    'code', flat=True)
            )
        )

def generate_enrolment_form(student):

    context = {
        'student': student,
        'allowed_courses': student.get_allowed_enrolments()
    }
    template = get_template('student_enrolment_form_template.tex', using='jinja2')
    rendered_tpl = template.render(context=context).encode('utf8')
    # Python3 only. For python2 check out the docs!
    if student.advisor == None:
        student.advisor = "بدون مشرف"
    directory = os.path.join(
        '/home/abdulhaq/workspace/pX/pX-tools/legacyDB/spring_2016/student_enrolment_forms/' +
        student.advisor
    )
    if not os.path.exists(directory):
        os.makedirs(directory)

    # with open(os.path.join(
    #     directory+'/'+student.registration_number+'.tex'),
    #         'w') as texfile:
    #     texfile.write(rendered_tpl)

    #tempdir = tempfile.mkdtemp()
    # Create subprocess, supress output with PIPE and
    # run latex twice to generate the TOC properly.
    # Finally read the generated pdf.
    for i in range(2):
        process = Popen(
            ['xelatex',
             '-jobname', ' '.join([student.full_name_ar, ' - ',
                                   student.registration_number]),
             '-output-directory', directory],
            stdin=PIPE,
            stdout=PIPE,
        )
        process.communicate(rendered_tpl)


def generate_academic_progress(student):
    three_last_periods = student.period_registrations.reverse()[:3]
    pass_rate_three = 0
    for period in three_last_periods:
        pass_rate_three += period.student_result.passed_credits/3.0
    context = {
        'student': student,
        'enrolments': student.get_enroled_courses(),
        'registrations': student.period_registrations.all(),
        'results': student.period_registrations.last().student_result,
        'pass_rate_three': pass_rate_three
    }
    template = get_template('student_academic_progress_template.tex',
                            using='jinja2')
    rendered_tpl = template.render(context=context).encode('utf8')
    # with open(os.path.join(
    #         '/home/abdulhaq/workspace/pX/pX-tools/legacyDB/tests/',
    #         's'+registration_number+'.tex'), 'w') as texfile:
    #     texfile.write(rendered_tpl)
    # Python3 only. For python2 check out the docs!
    if student.advisor == None:
        student.advisor = "بدون مشرف"
    directory = os.path.join(
    '/home/abdulhaq/workspace/pX/pX-tools/legacyDB/spring_2016/student_academic_progress/'+
    student.advisor
    )
    if not os.path.exists(directory):
        os.makedirs(directory)
    # #
    # with open(os.path.join(
    #     directory+'/'+student.registration_number+'.tex'),
    #         'w') as texfile:
    #     texfile.write(rendered_tpl)

    #tempdir = tempfile.mkdtemp()
    # Create subprocess, supress output with PIPE and
    # run latex twice to generate the TOC properly.
    # Finally read the generated pdf.
    for i in range(2):
        process = Popen(
            ['xelatex',
             '-jobname', ' '.join([student.full_name_ar, ' - ',
                                   student.registration_number]),
             '-output-directory', directory],
            stdin=PIPE,
            stdout=PIPE,
        )
        process.communicate(rendered_tpl)
