# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import apps

import factory
from factory import lazy_attribute

from faker import Factory as FakerFactory

# from pX.administration.courses.assessments.models import (
#     Assessment, AssessmentType)

faker = FakerFactory.create()
faker.seed(983843)


class Factory(factory.django.DjangoModelFactory):
    pass


class AssessmentFactory(Factory):

    class Meta:
        model = "assessments.Assessment"

    assessment_type = factory.SubFactory(
        "tests.factories.AssessmentTypeFactory")
    period_course = factory.SubFactory(
        "tests.factories.PeriodCourseFactory")
    total_grade = 20


class AssessmentTypeFactory(Factory):

    class Meta:
        model = "assessments.AssessmentType"
        #django_get_or_create = ("assessment_type",)

    assessment_type = factory.LazyAttribute(lambda x: faker.word())


class PeriodCourseFactory(Factory):

    class Meta:
        model = "courses.PeriodCourse"

    period = factory.SubFactory(
        "tests.factories.PeriodFactory")
    course = factory.SubFactory(
        "tests.factories.CourseFactory")


class PeriodFactory(Factory):

    class Meta:
        model = "periods.Period"

    period = factory.Iterator([1, 2, 3])
    academic_year = factory.Iterator(["2010,2011", "2011,2012",
                                      "2012,2013", "2013,2014"])


class CourseFactory(Factory):

    class Meta:
        model = "courses.Course"

    code = factory.Sequence(lambda n: "AE{}".format(n))
    name = factory.Iterator(["A/C Design", "Aerodynamics I",
                             "Mechanical Vibration", "Aerodynamics II"])
    department = factory.SubFactory("tests.factories.DepartmentFactory")
    credit = 3
    course_description = ''
    course_syllabus = ''

    @lazy_attribute
    def level(self):
        return int(self.code[2])*100


class DepartmentFactory(Factory):

    class Meta:
        model = "administration.Department"
        django_get_or_create = ("name", )

    acronym = ["AE"]
    name = "Department of Aeronautical Engineering"
    faculty = factory.SubFactory("tests.factories.FacultyFactory")
    domain_name = ''


class FacultyFactory(Factory):

    class Meta:
        model = "administration.Faculty"
        django_get_or_create = ("name", )

    name = "Faculty of Engineering"


class SectionEnrolmentFactory(Factory):

    class Meta:
        model = "section_enrolments.SectionEnrolment"

    section = factory.SubFactory("tests.factories.SectionFactory")
    period_registration = factory.SubFactory(
        "tests.factories.PeriodRegistrationFactory")


class SectionFactory(Factory):

    class Meta:
        model = "courses.Section"

    period_course = factory.SubFactory("tests.factories.PeriodCourseFactory")
    group = '1'


class PeriodRegistrationFactory(Factory):

    class Meta:
        model = "period_registrations.PeriodRegistration"

    student = factory.SubFactory("tests.factories.StudentFactory")
    period = factory.SubFactory("tests.factories.PeriodFactory")


class PersonFactory(Factory):

    class Meta:
        model = "users.Person"

    first_name = factory.LazyAttribute(lambda x: faker.first_name())
    last_name = factory.LazyAttribute(lambda x: faker.last_name())
    gender = 'M'


class StudentFactory(PersonFactory):

    class Meta:
        model = "students.Student"

    registration_number = factory.Sequence(lambda n: '0{}'.format(n))


class StudentWithPeriodRegistrationFactory(StudentFactory):

    periods = factory.RelatedFactory(PeriodRegistrationFactory, 'student')


class AssessmentResultFactory(Factory):

    class Meta:
        model = "assessments.AssessmentResult"

    assessment = factory.SubFactory("tests.factories.AssessmentFactory")
    section_enrolment = factory.SubFactory(
        "tests.factories.SectionEnrolmentFactory")
