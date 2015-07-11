# -*- coding: utf-8 -*-

import uuid
from django.db import models
from django.utils.translation import ugettext_lazy as _
from linguo.models import MultilingualModel
from linguo.managers import MultilingualManager
#from UIS.models.users import *
#from UIS.models.administration import Department
#from UIS.models.courses import CourseCatalogue
#from UIS.models.employees import *
#from UIS.models.students import
#from UIS.models.time_period import Period


class Degree(MultilingualModel):
    """

    The degree model is a bit tricky! because important design
    decisions have been included in it. For example, it's expected
    that the required credits for completing the Bachelor Degree in
    Aeronautical Engineering to change from 151/152 to 144. We simply
    CANNOT have the original degree changed! That is a SIN in database
    design. No words will be suitable to describe the catastrophes that
    will happen if something like this was allowed.

    random thoughts:

n    - what is the point of the department field?: well, to associate a
      degree with a department means that department officials will be
      able to edit this degree (in sane ways only) (perhaps this is related
      to the permission issue I need to search!)
    - WHAT IF a degree is associated with more than one department??
    - TODO: THINK OF TWO DEPARTMENT DEGREES
    - first_intake field: once credits_required field is changed, the
      degree MUST be given an appropriate alias, the first term this is
      offered is a good alias for a new degree.
    - TODO: MINOR DEGREES NEED TO BE CONSIDERED ALONG WITH
      GENERAL LEVEL ENGINEERING
    - each degree has to be related to its required courses via the
      many2many field, this is done in coursecatalouge!

    here is what I plan to do with minor degrees: (what I did!)

    * add a field to degrees that determines whether a degree is a major
      or not
    * if a degree is NOT major, then it MUST have minor(s)

       * for example, if we have a Bachelor Degree in EEE, that it self is not
         a major because they have minors, so major should be false and minors
         should point to minor degrees (in this case, power, communication
         etc..)
       * even a better example; general engineering (المرحلة العامة),
         that is not a major, its minors will be all engineering degrees!!

    further updates:

    * first_intake field is redundant, if a degree replaces another, the old
      degree should have an obsolete field set to true and the degree should
      be added to the 'replaced_degrees' field in the new degree.

    * after deleting the first_intake field, now uniqueness is simply
      name, department, and credits_required
    """

    degree_id = models.UUIDField(primary_key=True,
                                 default=uuid.uuid4,
                                 editable=False)

    objects = MultilingualManager()

    DEGREE_LEVELS = (
        ('U', _('Undergraduate')),
        ('P', _('Postgraduate')),
    )

    level = models.CharField(max_length=1, choices=DEGREE_LEVELS)
    name = models.CharField(max_length=60)
    credits_required = models.SmallIntegerField()
    department = models.ForeignKey('Department', blank=True,
                                   on_delete=models.PROTECT)
    is_major = models.BooleanField(default=True)
    is_obsolete = models.BooleanField(default=False)
    minors = models.ManyToManyField('self', blank=True)
    # first intake of this degree, requirements may change from year to year!
    first_intake = models.ForeignKey('Period',
                                     blank=True, null=True)
    replaced_degrees = models.ManyToManyField('self',
                                              blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        app_label = 'UIS'
        unique_together = (
            ('name', 'credits_required', 'department'),
        )
        translate = ('name', )

    def __unicode__(self):
        return self.name  # + _('First Intake') + \
    #         ' (' + str(self.first_intake) + ')' or self.name_en

    # def natural_key(self):
    #     return (self.name_en,) + self.department.natural_key() + \
    #         self.first_intake.natural_key()
    # natural_key.dependencies = ['Department', 'Term']


# class MinorDegree(models.Model):
#     """
#     THIS IS NOW OBSOLUTE, IT SHOULD BE DELETED

#     TODO: THIS NEEDS TO BE DELETED
#     """

#     objects = CommonNameManager()

#     degree = models.ForeignKey(Degree)
#     name_en = models.CharField(max_length=70)
#     name_ar = models.CharField(max_length=70)

#     def __unicode__(self):
#         return unicode(self.degree) + ' (' + self.name_en + ')'


class DegreeCourse(models.Model):
    """
    This represents the many2many relation between a degree and its
    required courses!
    """
    degree_course_id = models.UUIDField(primary_key=True,
                                        default=uuid.uuid4,
                                        editable=False)

    course = models.ForeignKey('CourseCatalogue',
                               blank=True,
                               on_delete=models.PROTECT)
    degree = models.ForeignKey('Degree', blank=True, on_delete=models.PROTECT)

    def __unicode__(self):
        return unicode(self.course) + ' ' + unicode(self.degree)

    class Meta:
        app_label = 'UIS'
        unique_together = ('course', 'degree',)
