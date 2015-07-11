# -*- coding: utf-8 -*-

import uuid
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _
from exclusivebooleanfield.fields import ExclusiveBooleanField
from UIS.managers import PeriodManager
from UIS.models.base_model import UISBaseModel
# from UIS.models.degrees import Degree


# class Period(TimeStamp):

#     ACADEMIC_YEAR = 'A'
#     TERM = 'T'
#     PERIOD_TYPE = (
#         (ACADEMIC_YEAR, _('Academic Year')),
#         (TERM, _('Term')),
#     )
#     period = models.IntegerField(choices=PERIOD_TYPE)
#     content_type = models.ForeignKey(ContentType)
#     object_id = models.PositiveIntegerField()
#     content_object = GenericForeignKey('content_type', 'object_id')

#     # academic_year = models.ForeignKey('AcademicYear',
#     #                                   on_delete=models.PROTECT)
#     # term = models.ForeignKey('Term', on_delete=models.PROTECT)
#     is_compulsary = models.BooleanField(default=True)
#     degrees = models.ManyToManyField('Degree', blank=True)
#     courses = models.ManyToManyField('CourseCatalogue',
#                                      through='PeriodCourse', blank=True)

#     class Meta:
#         app_label = 'UIS'
#         ordering = ['academic_year', ]


# class AcademicYear(TimeStamp):
#     """"""

#     academic_year = models.CommaSeparatedIntegerField(
#         max_length=9, verbose_name=_('academic year'), unique=True,
#         help_text=_('please enter the academic year in this format: \
#         for the year 2012-2013, enter: "2012,2013" (without quotes)'))
#     set_current_period = ExclusiveBooleanField(default=True)

#     objects = AcademicYearManager()

#     class Meta:
#         app_label = 'UIS'
#         ordering = ['academic_year', ]

#     def natural_key(self):
#         return self.academic_year

#     def __unicode__(self):
#         return self.academic_year


class Period(UISBaseModel):
    """
    an example of this model:
    if we're in the academic_year 2011-2012, we will have three terms:

    1. autumn 2011
    2. spring 2012
    3. summer 2012

    random thoughts:

    - if a student didn't register for a summer term, would the student be
      registered as dropped!!? What if the term is optional like what happened
      in Summer 2012? SO an is_compulsary field must be added to all terms
    - ماذا لو استيقظ أحد المسؤولين الكبار ذات صباح بمزاج متعكر وقرر عشوائيا
      وبدون دراسة (كسائر قرارات الدولة!) أن يغير نظام الدراسة إلى نظام سنة؟ أو
      بصفة عامة، هل من المهم إضافة كود للتعامل مع نظام السنة؟؟
      UPDATE, 18/02/15: let this **** do whatever he/she wants,computers handle
      everything!
    - term start/end dates? enrolment date? last date for deleting enrolments
       in courses? etc.. TODO: dates fields for terms
    """

    period_id = models.UUIDField(primary_key=True,
                                 default=uuid.uuid4,
                                 editable=False)

    objects = PeriodManager()
    ACADEMIC_YEAR = 0
    AUTUMN = 1
    SPRING = 2
    SUMMER = 3
    PERIOD = (
        (ACADEMIC_YEAR, _('Academic Year')),
        (AUTUMN, _('Autumn')),
        (SPRING, _('Spring')),
        (SUMMER, _('Summer')),
    )

    academic_year = models.CommaSeparatedIntegerField(
        max_length=9, verbose_name=_('academic year'),
        help_text=_('please enter the academic year in this format: \
        for the year 2012-2013, enter: "2012,2013" (without quotes)'))

    period = models.IntegerField(choices=PERIOD)
    # SCHEDULING NEEDS TO BE SOLVED ASAP
    # start_date = models.DateField(blank=True, null=True)
    # end_date = models.DateField(blank=True, null=True)
    # is_compulsary = models.BooleanField(default=True)
    # start/end dates and wheather a period is compulsary should be specific
    # to degrees!
    # degrees = models.ManyToManyField('Degree',
    #                                  through='PeriodDegree', blank=True)
    courses = models.ManyToManyField('CourseCatalogue',
                                     through='PeriodCourse', blank=True)

    # exclusivebooleanfield does not work when importing data, bug to be fixed!
    set_current_period = ExclusiveBooleanField(default=True)

    class Meta:
        app_label = 'UIS'
        unique_together = (
            ('academic_year', 'period'),
        )
        ordering = ['academic_year', 'period']

    def __unicode__(self):
        if self.period == 1:
            return self.get_period_display() + " " + \
                self.academic_year[:4]
        elif self.period in [2, 3]:
            return self.get_period_display() + " " + \
                self.academic_year[-4:]
        else:
            return self.get_period_display() + " " + self.academic_year

    def natural_key(self):
        return (self.academic_year, self.period)


class PeriodDegree(UISBaseModel):
    """"""
    period_degree_id = models.UUIDField(primary_key=True,
                                        default=uuid.uuid4,
                                        editable=False)
    period = models.ForeignKey('Period', on_delete=models.PROTECT)
    degree = models.ForeignKey('Degree', on_delete=models.PROTECT)
    is_compulsary = models.BooleanField(default=True)
    #here we define start/end dates

    class Meta:
        app_label = 'UIS'
        unique_together = (
            ('period', 'degree'),
        )
