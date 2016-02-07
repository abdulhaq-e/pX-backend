# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db.models import signals

import pytest
import factory

# from ..factories import (
#     AssessmentFactory, AssessmentTypeFactory, PeriodCourseFactory
# )
from ..utils import disconnect_signals, reconnect_signals

from pX.administration.courses.assessments.models import (
    Assessment, AssessmentType)
from pX.administration.courses.models import (
    Course, PeriodCourse)
from pX.administration.models import (
    Faculty, Department)
from pX.administration.periods.models import (
    Period)
from pX.users.models import (
    Person)
from pX.students.models import (
    Student)
from pX.students.section_enrolments.models import (
    SectionEnrolment)
from pX.students.period_registrations.models import (
    PeriodRegistration)

pytestmark = pytest.mark.django_db(transaction=True)


def setup_module():
    disconnect_signals()


def teardown_module():
    reconnect_signals()


@pytest.mark.isolatedtests
class TestFactories:

    def test_assessment_factory(self, assessment_factory):
        # print AssessmentType.objects.all()
        assessment_factory()

        assert Assessment.objects.all().count() == 1
        # assert AssessmentType.objects.all().count() == 1
        assert Course.objects.all().count() == 1
        assert PeriodCourse.objects.all().count() == 1
        assert Faculty.objects.all().count() == 1
        assert Department.objects.all().count() == 1

    def test_assessment_type_factory(self, assessment_type_factory):

        assessment_type_factory()

        assert AssessmentType.objects.all().count() == 1

    def test_period_course_factory(self, period_course_factory):

        period_course_factory()

        assert PeriodCourse.objects.all().count() == 1
        assert Period.objects.all().count() == 1
        assert Course.objects.all().count() == 1

    def test_section_factory(self, section_factory):

        section = section_factory()

        assert section.group == '1'
        assert PeriodCourse.objects.all().count() == 1

    def test_section_enrolment_factory(self, section_enrolment_factory):

        section_enrolment = section_enrolment_factory()

        assert SectionEnrolment.objects.all().count() == 1
        assert PeriodRegistration.objects.all().count() == 1

    def test_person_factory(self, person_factory):

        person = person_factory()

        assert person.gender == 'M'
        assert Person.objects.all().count() == 1

    def test_period_registration_factory(self, period_registration_factory):

        period_registration_factory()

        assert PeriodRegistration.objects.all().count() == 1
        assert Student.objects.all().count() == 1
        assert Period.objects.all().count() == 1

    def test_student_factory(self, student_factory):

        student = student_factory()

        assert student.gender == 'M'

    def test_student_with_period_registration_factory(
            self, student_with_period_registration_factory):

        student = student_with_period_registration_factory()

        assert student.periods.all().count() == 1

    def test_assessment_result_factory(self, assessment_result_factory):

        assessment_result = assessment_result_factory()

        assert assessment_result.grade is None
