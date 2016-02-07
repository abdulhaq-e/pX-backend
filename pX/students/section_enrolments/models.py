# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import uuid

from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from .managers import SectionEnrolmentManager
from ...base.models import pXBaseModel


@python_2_unicode_compatible
class SectionEnrolment(pXBaseModel):
    """
    represents the m2m relation between students and sections

    all the fun is here!
    """
    section_enrolment_id = models.UUIDField(primary_key=True,
                                            default=uuid.uuid4,
                                            editable=False)

    # def __init__(self, *args, **kwargs):

    #     super(SectionEnrolment, self).__init__(*args, **kwargs)
    custom = SectionEnrolmentManager()
    objects = models.Manager()
    # from_queryset(SectionEnrolmentQuerySet)
    # original = models.Manager()
    period_registration = models.ForeignKey(
        'period_registrations.PeriodRegistration',
        on_delete=models.PROTECT,
        related_name='studentenrolment')
    section = models.ForeignKey('courses.Section', on_delete=models.PROTECT,
                                related_name='studentenrolment')
    sub_sections = models.ManyToManyField('courses.SubSection',
                                          through='SubSectionEnrolment',
                                          blank=True)
    # carry_marks = models.FloatField(blank=True, null=True,
    # validators=[validate_grade])
    # final_exam = models.FloatField(blank=True, null=True,
    # validators=[validate_grade])
    grade = models.FloatField(null=True)
    # validators=[validate_grade])
    # if the results are published or not!
    # published = models.BooleanField(default=False)
    '''
    THERE SHOULD BE A VALIDATOR TO MAKE SURE SECTION__PERIOD ==
    PERIOD_REGISTRATION__PERIOD
    '''

    class Meta:
        unique_together = ('period_registration', 'section')
        ordering = ('period_registration',)

    def __str__(self):
        return '{} {}'.format(self.section, self.period_registration)

    # @property
    # def grade(self):
    #     total = self.assessment_results.get(
    #         assessment__assessment_type__assessment_type='Total')

    #     return total.grade




class SectionEnrolmentLog(pXBaseModel):
    """
    a temp. table to store added/deleted enrolment, until I
    find a better solution
    """
    section_enrolment_log_id = models.UUIDField(primary_key=True,
                                    default=uuid.uuid4,
                                    editable=False)

    period_registration = models.ForeignKey('period_registrations.PeriodRegistration',
                                on_delete=models.PROTECT,
                                related_name='studentenrolmentlog')
    section = models.ForeignKey('courses.Section', on_delete=models.PROTECT,
                                related_name='studentenrolmentlog')
    STATUS = (
        ('A', 'Added'),
        ('D', 'Dropped'),
    )
    enrolment_status = models.CharField(
        max_length=1,
        choices=STATUS,
        default='A')

    class Meta:
        unique_together = ('period_registration', 'section',
                           'enrolment_status')

    def __unicode__(self):
        return (unicode(self.student_registration) + ' '
                + str(self.section) + ' ' + str(self.enrolment_status))


class SubSectionEnrolment(pXBaseModel):

    sub_section = models.ForeignKey("courses.SubSection",
                                    on_delete=models.PROTECT)
    enrolment = models.ForeignKey("section_enrolments.SectionEnrolment")
