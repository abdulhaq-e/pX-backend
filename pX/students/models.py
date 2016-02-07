# -*- coding: utf-8 -*-
from __future__ import division, unicode_literals

import uuid

from copy import deepcopy
from collections import OrderedDict

from django.db import models, IntegrityError
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.fields import GenericRelation
from django.core.urlresolvers import reverse

# from django.db.models import Q, F, Sum

from .utils import calculate_results
from .temp_models import StudentResult
from ..base.models import pXBaseModel
from ..users.models import Person
from .period_registrations.models import PeriodRegistration
# from ..periods.models import Period
# from ..courses.models import Course, CoursePrerequisite
# from ..enrolments.models import StudentEnrolment



# from UIS.models.student_utils import get_results
# from UIS.models.administration import Department
# from UIS.models.courses import Section
# from UIS.models.degrees import Degree
# from UIS.models.employees import Employee
# from UIS.models.time_period import Period
#from UIS.models.users import, UISUser


class Student(Person):
    """

    random thoughts:

    * I really don't know what's the purpose of the STATUS field?
      I should delete it if I don't know what it means but i just don't
      feel like it, perhaps a 'GRADUATED' status can be added, emm, so
      Enrolled means the student is still not finished and graduated means
      he is finished!

     oh wait!, perhaps this can be used for إخلاء طرف or منقطعين

     a decision needs to be made fast!

    * Regarding the get_results function, this needs to be the most beautiful
      function in this whole code! It's not complete yet, so I'll document it
      later!

    * should the registration_number have a leading zero (022fjdsfljsd) ??

      maybe store the number in database without a leading zero but add it when
      displaying the number

    * TODO: Now I'm thinking too much: students taking two majors? why not?

    * a many2many relation with terms and enrolments has been added to
      this model, ALL MODELS THAT HAVE TWO FOREIGN KEYS ARE LIKELY TO BE
      A THROUGH TABLE FOR a many2many relation. THIS RELATIONS NEEDS TO BE
      ADDED TO ONE OF THE MODELS THE FOREIGN KEY IS REFERRING TO.

    """

    #objects = StudentQuerySet.as_manager()

    student_id = models.UUIDField(primary_key=True,
                                  default=uuid.uuid4,
                                  editable=False)

    # user = GenericRelation('UserProfile',
    #                        content_type_field='profile_type',
    #                        object_id_field='profile_id')
    STATUS = (
        ('E', 'Enrolled'),
        ('G', 'Graduated'),
        ('L', 'Left'),  # إخلى طرفه
        ('D', 'Dropped Out'),  # منقطع
        ('T', 'Transferred'),
        ('K', 'Kicked Out')
    )
    details = models.OneToOneField(Person, parent_link=True)
    registration_number = models.CharField(unique=True, max_length=255,
                                              verbose_name=_('Student UUID'))
    status = models.CharField(max_length=1, choices=STATUS, default='E')
    # can a student enroll in more than one degree,
    # perhaps a postgrad using the same UUID
    periods = models.ManyToManyField('periods.Period',
                                     through=PeriodRegistration,
                                     blank=True,
                                     related_name='students')
    # the below advisor field is EXTREMELY TEMPORARY
    advisor = models.CharField(max_length=200, null=True,
                               blank=True)

    #THIS WILL BE A HUGE UPDATE: 17/02/15K approx 23:00, I think all the below fields show exists in the student registration model because then degree changes can be tracked (it was stupid having one choice only!!!) and enrollments can be finally related to student registraion, and finally; if advisors change, we have some history!!

    #UPDATE 22/02/15: the enrolment m2m needs to be here, it can't be related
    #to student_registration. Why: because a section might have an associated
    #period that is different from the registered_period. In other words, by
    #having the studentenrolment to relate sections and studentregistration,
    #integrity problem will occur because of these have a relation to period!

    #here I come again on the evening of the 22/03/15 at 10:18 pm to discuss
    #where to put enrolments. It's a coincidence that I come here after a month
    #from bringing them back to the students model. Now, I will discuss, with
    #myself what are the benefits of both locations:
    #1- making a query on student enrolment:
    # a) using studentregistration: StudentEnrolment.objects.filter(studenregistration__student=blabla)
    # b) using student: StudentEnrolment.objects.filter(student=blabla)
    #2- HOWEVER< this won't be possible when using student reg:
    #   student.studenenrolment.blablabla
    #3- WHY DO I NEED studentenrolment in studentreg in the first place?
    # it's to make sure no enrolments are made without a registration!
    # much better than having some kind of validation
    # the only validation is input validation which should make sure that
    # the section period is equal to the registration period.
    #LETS GO
    # user_type = GenericRelation('UserType', related_query_name='students')

    class Meta:
        pass

    def calculate_results(self):
        if StudentResult.objects.filter(
            period_registration__student=self).exists():
            StudentResult.objects.filter(
                period_registration__student=self).delete()

        calculate_results(self)

'''
THE PARAGRAPH BELOW TRIES TO EXPLAIN MY THOUGHTS

I WILL HAVE A STUDENT_DEGREE TABLE/MODEL WHICH WILL STORE ALL TYPES OF GRADES

THEN DEPENDING ON THE ENROLMENT_STATUS (WHICH IS A FIELD IN THE STUDENT_ENROLMENT

TABLE), THE GRADE IN THE STUDENT_ENROLMENT WILL BE SET, FOR EXAMPLE, IF IT IS

"CREDITS WITHELD", THE STUDENT_ENROLMENT GRADE WILL BE NULL EVEN THOUGH IN THE

STUDENT GRADE TABLE, IT'S VALUE WILL NOT BE NULL!

THE STUDENT GRADE TABLE WILL ALSO HOLD CHANGES TO GRADES.
'''




class StudentAllowedEnrolment(models.Model):
    '''
    THIS SHOULD BE A MATERIALIZED VIEW, I DON'T LIKE THE CURRENT IMPLEMENTATION.
    '''
    student_allowed_enrolments_id = models.UUIDField(primary_key=True,
                                                     default=uuid.uuid4,
                                                     editable=False)

    student = models.ForeignKey('Student', related_name='allowed_enrolment')
    course = models.ForeignKey("courses.Course")
    # permitted = models.BooleanField(default=True)
    # primary = models.BooleanField(default=True)
