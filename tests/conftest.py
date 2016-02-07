import pytest
from pytest_factoryboy import register

from .factories import (
    AssessmentFactory, AssessmentTypeFactory, PeriodCourseFactory,
    PeriodFactory, DepartmentFactory, FacultyFactory, CourseFactory,
    SectionFactory, SectionEnrolmentFactory, PersonFactory,
    PeriodRegistrationFactory, StudentFactory,
    StudentWithPeriodRegistrationFactory, AssessmentResultFactory,)


register(AssessmentFactory)
register(AssessmentTypeFactory)
register(PeriodCourseFactory)
register(PeriodFactory)
register(DepartmentFactory)
register(FacultyFactory)
register(CourseFactory)
register(SectionFactory)
register(SectionEnrolmentFactory)
register(PersonFactory)
register(PeriodRegistrationFactory)
register(StudentFactory)
register(StudentWithPeriodRegistrationFactory)
register(AssessmentResultFactory)
