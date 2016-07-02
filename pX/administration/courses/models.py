# -*- coding: utf-8 -*-
#from __future__ import unicode_literals

import uuid

from django.db import models
from django.utils.translation import ugettext_lazy as _

from ...base.models import pXBaseModel


class Course(pXBaseModel):
    '''
    an extremely important model, lots of design decisions

    this is the basic idea:

    - a course is simply a course! with a name and a code!
    - IF the course credits/prerequisites changed, a NEW COURSE must be
      added, THIS IS A MUST!
    - to differentiate between courses (not in the database level since that
      is taken care of by the primary key), a first_term_taught and
      last_term_taught fields were initially added
    - this breaks some of the rules indicated on that great database
      design book, first_term_taught and last_term_taught are CALCULATED
      FIELDS, they shouldn't be here at all.
    - but then: how are two courses (with the same code) different?
      well, they have different credits that are different
    - how to make sure that when adding courses to a term that for example:
      the old AE325 which is worth 2 credits doesn't appear along with the new
      AE325 which is worth 3 credits!? I DON'T KNOW THE BEST ANSWER TO THIS
      QUESTION!
    - how to handle elective courses (answer in equalled_coursess field)
    - add documentation for equalled_coursess field:

      there are many uses for this field:

      1. when two courses are similar ,usually one of them only has to be
         taken, so something like this would be in the degree requirements:
         MIT18.02 or MIT18.022 are required. Technically, they are both
         compulsary but taking one will waive the other!, how is this done? We
         add them both as equalled_coursess to each other and in the code
         we handle this case: TWO SYMMETRICALLY EQUALLED_COURSES COURSES
         BELONGING TO THE SAME DEGREE.
      2. the answer to the question above is: mark the old course as not_active
         (is_not_active=True) and ADD the course as equalled_courses
         for the new course

         BUT A PROBLEM ARISES NOW: HOW CAN UNIQUENESS BE APPLIED??

         code & name & credit is certainly not the way to do it
         adding prerequisites field to the above will enforce uniqueness but
         because prerequisites is an m2m field, it cannot be used in
         unique_together, either a through table have to be used OR signals
         no way I'm going to use a through table for prerequisites but I should
         read on signals, maybe that's the way to do it?

         TODO: uniqueness need to be defined using code, name_en, credit,
         prerequisites

         ALL THE ABOVE RAMBLING IS LEFT FOR HISTORICAL PURPOSES,
         HERE IS THE **** SOLUTION:

         UNIQUENESS IS SIMPLY DEFINED FOR CODE, NAME_EN, and is_not_active (and
         department obviously!)

         Very simple: why would a department have two courses with the same
         code and they're both ACTIVE??

         UPDATE 18/02/15: is_not_active has been changed to is_obsolete

      3. elective courses: they will obviously have is_compulsary set to False.
         all elective courses should be equalled_courses to each other (must be
         handled when adding electives)

    other random thoughts:

    - the notes field is for notes lol
    - course description and syllabus should NOT go here, in our institutions
      these WILL definitely change and changes to course catalogue should only
      be made when credits/prerequisites change (and that's why the description
      and syllabus should go in the term course with the ability to set them as
      default)

    UPDATES TO THE ABOVE RAMBLING (20/02/15):

    - the first_taught IS NEEDED for uniqueness, along with last_taught and
      is_obsolete, my original idea was correct, or so I hope!.
    '''

    course_id = models.UUIDField(primary_key=True,
                                 default=uuid.uuid4,
                                 editable=False)

    code = models.CharField(max_length=20)
    level = models.SmallIntegerField(null=True)
    name = models.CharField(max_length=200, blank=True,
                               verbose_name=_('Course name'))
    # is_compulsary = models.BooleanField(default=True)
    is_obsolete = models.BooleanField(default=False)
    # first_taught and last_taught and is_compulsary removed 29/08/15
    # is_compulsary should probably go to DegreeCourse
    # first_taught = models.ForeignKey('Period',
    #                                  verbose_name=_('First period given'),
    #                                  on_delete=models.PROTECT,
    #                                  blank=True, null=True,
    #                                  related_name='first_taught_set')
    # last_tught = models.ForeignKey('Period',
    #                                verbose_name=_('Last period given'),
    #                                blank=True, null=True,
    #                                on_delete=models.PROTECT,
    #                                related_name='last_taught_set')
    department = models.ForeignKey('administration.Department', blank=True,
                                   on_delete=models.PROTECT)
    credit = models.SmallIntegerField()
    degrees = models.ManyToManyField('degrees.Degree',
                                     through='DegreeCourse',
                                     blank=True,
                                     related_name='courses')
    periods = models.ManyToManyField('Course',
                                     through='PeriodCourse',
                                     blank=True,
                                     related_name='available_periods')

    prerequisite_courses = models.ManyToManyField('self', symmetrical=False,
                                           blank=True,
                                           #related_name='required_for',
                                           through='CoursePrerequisite')
    equalled_courses = models.ManyToManyField('self', symmetrical=False,
                                              blank=True,
                                              related_name='equalled_with')
    course_description = models.TextField(blank=True)
    course_syllabus = models.TextField(blank=True)

    def __unicode__(self):
        return ' '.join([self.code, ' ', self.name_en])

    class Meta:
        unique_together = (
            ('code', 'name', 'department', 'credit',)
        )
        ordering = ['level', 'code']
        verbose_name = 'Course Catalogue'
        verbose_name_plural = 'Course Catalogue'


class CoursePrerequisite(pXBaseModel):

    course = models.ForeignKey('Course', related_name='prerequisites')
    prerequisite = models.ForeignKey('Course', related_name='required_for')

    def __unicode__(self):
        return ' '.join(['Course:', str(self.course),
                ', Prerequisite:', str(self.prerequisite)])


class DegreeCourse(pXBaseModel):
    """
    This represents the many2many relation between a degree and its
    required courses!
    """
    degree_course_id = models.UUIDField(primary_key=True,
                                        default=uuid.uuid4,
                                        editable=False)

    course = models.ForeignKey('Course',
                               blank=True,
                               on_delete=models.PROTECT)
    degree = models.ForeignKey('degrees.Degree',
                               blank=True,
                               on_delete=models.PROTECT)

    def __unicode__(self):
        return unicode(self.course) + ' ' + unicode(self.degree)

    class Meta:
        unique_together = ('course', 'degree',)


class PeriodCourse(pXBaseModel):
    """

    represents the m2m relationship between periods and courses
    i.e. which courses are available in a period (academic_year or term)

    description/syllabus should go  here as indicated in the course catalogue
    docs

    other fields might also be important, course outcome and the likes.
    """
    #objects = TermCourseManager()
    period_course_id = models.UUIDField(primary_key=True,
                                        default=uuid.uuid4,
                                        editable=False)

    period = models.ForeignKey('periods.Period')
    course = models.ForeignKey('Course')
    #exclude_from_prerequisites = models.BooleanField(default=False)
    # the above SHOULd restrict if the main and secondary sections should
    # have the same groups (a check needs to be done to ensure main sections
    # have the same groups as secondary sections
    shared_groups = models.BooleanField(default=False)

    section_types = models.ManyToManyField('SubSectionType',
                                           through='PeriodCourseSubSection')

    class Meta:
        unique_together = ('period', 'course',)

    def __unicode__(self):
        return ' '.join([unicode(self.course), "(",
                         unicode(self.period), ")"])


class SubSectionType(pXBaseModel):
    """
    i forgot why i need this:
    penso che: this defines what are the sections,
    e.g. main, exam, tutorial, lab, whatever,
    MAIN SHOULD BE COMPULSARY FOR ALL PERIOD COURSES
    """

    section_type_id = models.UUIDField(primary_key=True,
                                  default=uuid.uuid4,
                                  editable=False)

    name = models.CharField(max_length=40)

    class Meta:
        pass


class PeriodCourseSubSection(pXBaseModel):
    """
    similar to the below model, i forgot what this is:
    penso che: this lets us define something like:
    GS200, it has three sections (for example):
    a main section: compulsary enrolment!
    a tutorial section: non-compulsary.
    a lab: compulsary!
    """
    period_course_section_id = models.UUIDField(primary_key=True,
                                                default=uuid.uuid4,
                                                editable=False)

    period_course = models.ForeignKey('PeriodCourse')
    section_type = models.ForeignKey('SubSectionType')
    is_compulsary = models.BooleanField(default=True)

    class Meta:
        pass


class Section(pXBaseModel):
    """

    another important model, what is the difference between period courses and
    sections?

    well, sections define something like a period, it can be assigned a group
    etc ...

    now to the random notes:

    - why have a name field?:

      say we have GS200, it has lectures, tutorials (imagine it does!) and labs
      they will all be assigned a different section so a unique name must be
      given. BUT we really can't have student enrolling in GS200 lectures and
      not enrolling in labs/tutorials.

      THAT'S WHY WE HAVE the associated_section m2m field, the main GS200
      section will have the lab/tutorial section as associated_sections

      But we also can't have a student enrolling in labs/tutorial without
      enrolling in lectures, that's even more stupid than the first case!
      so we define an is_main field which is set to true for all main sections!
      thus students can only enrol in main sections and IF THAT section has
      associated_sections, they will be able to enrol in them!

      so when enrolling, a certain piece of code enforces the student to enrol
      in the lab/tutorial as well

    - time_table needs to be seriously reviewed, TODO: REVIEW TIME TABLE
      RESERVATION FOR SECTIONS, THINK OF INTEGRATION WITH django-scheduler

    - limit: groups will have certain limits, initially the limit was assigned
      to departments but that's so stupid, it's a much better idea to assign
      it to degrees!

      This creates a new problem though, in fact, that's why I had it assigned
      to department in the first place. The problem is: if there are two Aero
      degrees for example, how to combine them together in a single limit.
    """

    # objects = SectionManager()

    section_id = models.UUIDField(primary_key=True,
                                  default=uuid.uuid4,
                                  editable=False)

    # period_course = models.ForeignKey('PeriodCourse', blank=True,
    #                                   on_delete=models.PROTECT)
    period_course = models.ForeignKey(
        'PeriodCourse',
        on_delete=models.PROTECT
    )

    name = models.CharField(max_length=15,
                            blank=True)

    group = models.CharField(max_length=10,
                             blank=True)

    class Meta:
        unique_together = (
            ('period_course', 'group'),
        )

# class SectionLimit(models.Model):
#     """
#     represents the m2m relation between degrees and sections

#     random thoughts again:

#     - TODO: think of how to choose all related degrees regardless
#       of their requirements/credits bla bla bla.
#     """
#     section = models.ForeignKey('Section',
#                                 on_delete=models.PROTECT)
#     degree = models.ForeignKey('Degree',
#                                on_delete=models.PROTECT, blank=True, null=True)
#     limit = models.SmallIntegerField(verbose_name=_('limit'))

#     class Meta:
#         app_label = 'UIS'
#         unique_together = ('section', 'degree',)


# class SectionInstructor(models.Model):
#     """
#     represents the m2m relation between instructors and sections

#     TODO: permission review, a must do
#     """
#     instructor = models.ForeignKey('Employee', on_delete=models.PROTECT)
#     section = models.ForeignKey('Section', on_delete=models.PROTECT)
#     role = models.CharField(max_length=20)

#     class Meta:
#        pass

class SubSection(pXBaseModel):

    sub_section_id = models.UUIDField(primary_key=True,
                                  default=uuid.uuid4,
                                  editable=False)

    # period_course = models.ForeignKey('PeriodCourse', blank=True,
    #                                   on_delete=models.PROTECT)
    section_type = models.ForeignKey(
        'PeriodCourseSubSection',
        blank=True,
        on_delete=models.PROTECT
    )

    name = models.CharField(max_length=15,
                            blank=True)

    group = models.CharField(max_length=10,
                             null=True,
                             blank=True)

    class Meta:
        unique_together = (
            ('section_type', 'group'),
        )

    def __unicode__(self):
        return unicode(self.section_type.period_course) + ' Group ' + self.group + ' '
