# -*- coding: utf-8 -*-

from django.db import models
from django.db.models import F
from linguo.managers import MultilingualManager
from UIS.querysets import StudentEnrolmentQuerySet


class StudentEnrolmentManager(models.Manager.from_queryset(
        StudentEnrolmentQuerySet)):
    def get_queryset(self):
        return super(StudentEnrolmentManager, self).get_queryset().annotate(
            code=F('section__section_type__period_course__course__code'),
            course=F('section__section_type__period_course__course'),
            name=F('section__section_type__period_course__course__name'),
            name_ar=F('section__section_type__period_course__course__name_ar'),
            group=F('section__group'),
                #GRADE=F('grade'),
            credit=F('section__section_type__period_course__course__credit'),
            period=F('section__section_type__period_course__period')
        )


class MultilingualNameManager(MultilingualManager):
    """"""
    def get_by_natural_key(self, name):
        return self.get(name=name)


class MultilingualDeptManager(MultilingualManager):
    """"""
    def get_by_natural_key(self, name, faculty):
        return self.get(name=name,
                        faculty__name=faculty)


class MultilingualCourseManager(MultilingualManager):
    """"""
    def get_by_natural_key(self, code, department, is_obsolete):
        return self.get(code=code, department=department,
                        is_obsolete=is_obsolete)


class PeriodManager(models.Manager):
    """"""

    def get_by_natural_key(self, academic_year, period):
        return self.get(academic_year=academic_year, period=period)

    def get_from_url(self, period, academic_year):
        academic_year = academic_year.replace('-', ',')
        return self.get(period=period, academic_year=academic_year)


#might be obsolete
class PeriodCourseManager(models.Manager):
    """"""

    def get_by_natural_key(self, term, course):
        return self.get(term=term, course=course)


class SectionManager(models.Manager):
    """"""

    def get_by_natural_key(self, course, group):
        return self.get(course=course, group=group)
