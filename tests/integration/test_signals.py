# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db.models import Q

import pytest

from ..factories import (PeriodCourseFactory, )

pytestmark = pytest.mark.django_db

# def test_assessment_type_signals():

#     test1 = Q(assessment_type__assessment_type='Course Work')
#     test2 = Q(assessment_type__assessment_type='Final Examination')
#     assert AssessmentType.objects.count() == 2
#     #assert AssessmentType.objects.filter(test1 & test2).exists()


def test_period_course_assessments_signal(period_course_factory):

    course = period_course_factory()

    assert course.assessments.count() == 2
    assert course.assessments.filter(
        assessment_type__assessment_type='Course Work').count() == 1
    assert course.assessments.filter(
        assessment_type__assessment_type='Final Examination').count() == 1


def test_assessment_result_status_signal(assessment_result_factory):

    # initiate the result factory with a grade of 19
    assessment_result = assessment_result_factory(_grade=19)

    # the hidden grade is saved but grace should be None
    assert assessment_result._grade == 19
    assert assessment_result.grade is None

    # now change the assessment to Published
    assessment = assessment_result.assessment
    assessment.result_status = 'P'
    assessment.save()

    # reload the result from the db and see if grade is updated
    assessment_result.refresh_from_db()
    assert assessment_result.grade == 19

    # lets put the assessment on hold and see if grade become None
    assessment.result_status = 'O'
    assessment.save()

    assessment_result.save()
    assessment_result.refresh_from_db()

    assert assessment_result.grade is None
