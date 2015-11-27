# -*- coding: utf-8 -*-
import uuid

from django.db import models

from ..base.models import UISBaseModel
from ..enrolments.managers import StudentEnrolmentManager


class StudentEnrolment(UISBaseModel):
    """
    represents the m2m relation between students and sections

    all the fun is here!
    """
    enrolment_id = models.UUIDField(primary_key=True,
                                    default=uuid.uuid4,
                                    editable=False)

    # def __init__(self, *args, **kwargs):

    #     super(StudentEnrolment, self).__init__(*args, **kwargs)
    objects = StudentEnrolmentManager()
    # from_queryset(StudentEnrolmentQuerySet)
    original = models.Manager()
    student_registration = models.ForeignKey('StudentRegistration',
                                             on_delete=models.PROTECT,
                                             related_name='studentenrolment')
    section = models.ForeignKey('Section', on_delete=models.PROTECT,
                                related_name='studentenrolment')
    carry_marks = models.FloatField(blank=True, null=True,
                              validators=[validate_grade])
    final_exam = models.FloatField(blank=True, null=True,
                              validators=[validate_grade])
    grade = models.FloatField(blank=True, null=True,
                              validators=[validate_grade])
    # if the results are published or not!
    published = models.BooleanField(default=False)

    class Meta:
        app_label = 'UIS'
        unique_together = ('student_registration', 'section')
        ordering = ('student_registration',)

    def __unicode__(self):
        return (unicode(self.student_registration) + ' '
                + str(self.section) + str(self.grade))


class StudentEnrolmentLog(UISBaseModel):
    """
    a temp. table to store added/deleted enrolment, until I
    find a better solution
    """
    enrolment_log_id = models.UUIDField(primary_key=True,
                                    default=uuid.uuid4,
                                    editable=False)

    student_registration = models.ForeignKey('StudentRegistration',
                                on_delete=models.PROTECT,
                                related_name='studentenrolmentlog')
    section = models.ForeignKey('Section', on_delete=models.PROTECT,
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
        app_label = 'UIS'
        unique_together = ('student_registration', 'section',
                           'enrolment_status')

    def __unicode__(self):
        return (unicode(self.student_registration) + ' '
                + str(self.section) + ' ' + str(self.enrolment_status))
