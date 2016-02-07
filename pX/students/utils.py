# -*- coding: utf-8 -*-
from __future__ import division, unicode_literals

from django.db.models import Q

from .section_enrolments.models import SectionEnrolment
from .temp_models import StudentResult


def _update_results(period_registration, data):
    return StudentResult.objects.create(
        period_registration=period_registration, **data)


def calculate_results(student):
    """
    needs to be documented!
    """

    # StudentResult.objects.filter(
        #period_registration__student=student).delete()
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
             ('actual_period_count', actual_period_count),
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
                    pk__in=repeated_enrolments_distinct.values_list('pk', flat=True))
                #results[j]['Enrolments'] = period_enrolments
                #results[j]['Repeated Enrolments'] = repeated_enrolments

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
