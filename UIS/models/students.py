# -*- coding: utf-8 -*-

from __future__ import division
from copy import deepcopy
from django.db import models, IntegrityError
from django.utils.translation import ugettext_lazy as _
from pX import settings
import uuid
from django.core.urlresolvers import reverse
from collections import OrderedDict
#from UIS.querysets import StudentEnrolmentQuerySet
from UIS.validators import validate_grade
from django.db.models import F, Sum
from UIS.managers import StudentEnrolmentManager
from UIS.models.time_period import Period, PeriodDegree
from UIS.models.courses import CourseCatalogue
from UIS.models.users import Person
from django.contrib.contenttypes.fields import GenericRelation
from UIS.models.base_model import UISBaseModel
#from UIS.models.administration import Department
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
    # def __init__(self, *args, **kwargs):
    #     self.first_name = kwargs.pop('first_name', None)
    #     self.last_name = kwargs.pop('last_name', None)
    #     self.email = kwargs.pop('email', None)
    #     super(Student, self).__init__(*args, **kwargs)

    #objects = StudentQuerySet.as_manager()

    student_id = models.UUIDField(primary_key=True,
                                  default=uuid.uuid4,
                                  editable=False)

    user = GenericRelation('UserProfile',
                           content_type_field='profile_type',
                           object_id_field='profile_id')
    STATUS = (
        ('E', 'Enrolled'),
        ('G', 'Graduated'),
        ('D', 'Dropped Out')
    )
    details = models.OneToOneField(Person, parent_link=True)
    registration_number = models.CharField(unique=True, max_length=255,
                                              verbose_name=_('Student UUID'))
    status = models.CharField(max_length=1, choices=STATUS, default='E')
    # high_school_degree_location = models.CharField(max_length=15)
    # can a student enroll in more than one degree,
    # perhaps a postgrad using the same UUID
    periods = models.ManyToManyField('PeriodDegree',
                                     through='StudentRegistration',
                                     related_name='students')
    # advisor = models.ForeignKey('Employee', blank=True,
    #                                  on_delete=models.PROTECT,
    #                                  verbose_name=_('Academic Advisor'))

    #THIS WILL BE A HUGE UPDATE: 17/02/15K approx 23:00, I think all the below fields show exists in the student registration model because then degree changes can be tracked (it was stupid having one choice only!!!) and enrollments can be finally related to student registraion, and finally; if advisors change, we have some history!!
    # degree = models.ForeignKey('Degree', on_delete=models.PROTECT)
    # enrolments = models.ManyToManyField('Section',
    #                                     through='StudentEnrolment', blank=True)
    # advisor = models.ForeignKey('Employee', blank=True,
    #                             on_delete=models.PROTECT,
    #                             verbose_name=_('Academic Advisor'))
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

    # def save(self, *args, **kwargs):

    #     self.email = '0' + str(self.registration_number) + '@students.uot.edu.ly'

    #     super(Student, self).save(*args, **kwargs)
    #     # Call the "real" save() method.
    #     ut = UserType.objects.create(content_object=self)
    #     UISUser.objects.create_user(user_type=ut, email=self.email,
    #                                 first_name=self.first_name,
    #                                 last_name=self.last_name,
    #                                 password=self.registration_number)

    def __update_results(self, student_registration, data):
        result = StudentResult.objects.create(
            student_registration=student_registration, **data)

    def get_results(self):
        """
        needs to be documented!
        """
        # delete things first:
        StudentResult.objects.filter(student_registration__student=self).delete()
        # term = Term.objects.get(pk=1)
        all_enrolments = StudentEnrolment.objects.filter(
            student_registration__student=self).enroled()
        enrolments = all_enrolments.filter(
            student_registration__registration_type='R'
        )
        student_registrations = StudentRegistration.objects.filter(
            student=self
        )
        period_count = 0
        j = 0
        actual_period_count = period_count
        for i in student_registrations:

            if not StudentEnrolment.objects.filter(student_registration=i).exists() and i.registration_type not in ['DS', 'ES', 'NS']:
                i.registration_type = 'D'
                i.save()

            period_count += 1
            if i.registration_type in ['DS', 'ES', 'NS']:
                actual_period_count += 0
            else:
                actual_period_count += 1

            data = dict(
                [('period_count', period_count),
                 ('actual_period_count', actual_period_count),
                ]
            )

            if j == 0:
                if i.registration_type == 'R':
                    period_enrolments = enrolments.filter(
                        student_registration=i
                    )
                    repeated_enrolments = enrolments.none()
                    data.update(
                        period_enrolments.get_statistics(
                            credits='registered_credits',
                            points='scored_points').items() +
                        period_enrolments.passed().get_statistics(
                            credits='passed_credits',
                            points='passed_points').items() +
                        repeated_enrolments.get_statistics(
                            credits='repeated_credits',
                            points='repeated_points').items()
                    )
                    try:
                        data.update({
                            'GPA':
                            round(data['scored_points'] /
                                  data['registered_credits'], 2)
                        })
                    except ZeroDivisionError:
                        data.update({
                            'GPA': 0.0
                        })
                    data.update({
                        'cumulative_scored_points':
                        data['scored_points'],
                        'cumulative_registered_credits':
                        data['registered_credits'],
                        'cumulative_passed_credits':
                        data['passed_credits']})
                    try:
                        data.update({
                            'cumulative_GPA':
                            round(data['cumulative_scored_points'] /
                                  data['cumulative_registered_credits'], 2)
                        })
                    except ZeroDivisionError:
                        data.update({
                            'cumulative_GPA': 0.0
                        })

                    self.__update_results(i, data)
                elif i.registration_type in ['D', 'DS', 'ES', 'NS']:
                    data.update({
                        'registered_credits': 0.0,
                        'scored_points': 0.0,
                        'passed_credits': 0.0,
                        'passed_points': 0.0,
                        'repeated_credits': 0.0,
                        'repeated_points': 0.0,
                        'GPA': 0.0,
                        'cumulative_scored_points': 0.0,
                        'cumulative_registered_credits': 0.0,
                        'cumulative_passed_credits': 0.0,
                        'cumulative_GPA': 0.0
                    })
                    self.__update_results(i, data)
            elif j != 0:
                if i.registration_type in ['D', 'DS', 'ES', 'NS']:
                    previous_result = StudentResult.objects.get(
                        student_registration=student_registrations[j-1])
                    data.update({
                        'registered_credits': 0.0,
                        'scored_points': 0.0,
                        'passed_credits': 0.0,
                        'passed_points': 0.0,
                        'repeated_credits': 0.0,
                        'repeated_points': 0.0,
                        'GPA': 0.0,
                        'cumulative_scored_points': previous_result.cumulative_scored_points,
                        'cumulative_registered_credits': previous_result.cumulative_registered_credits,
                        'cumulative_passed_credits': previous_result.cumulative_passed_credits,
                        'cumulative_GPA': previous_result.cumulative_GPA
                    })
                    self.__update_results(i, data)

                    # except IntegrityError:

                    #     # data.update({
                    #     #     'student_registration': i}
                    #     print 'hah'
                    #     self.__update_results(i, data)
                elif i.registration_type == 'R':
                    period_enrolments = enrolments.filter(
                        student_registration=i
                    )
                    repeated_enrolments_distinct = enrolments.failed().filter(
                        code__in=period_enrolments.values_list(
                            'code', flat=True)).filter(
                                student_registration__in=[x for x in student_registrations[:j]]
                    ).order_by(
                        'section__section_type__period_course__course__code',
                        '-section__section_type__period_course__period'
                    ).distinct('section__section_type__period_course__course__code')

                    repeated_enrolments = StudentEnrolment.objects.filter(
                        pk__in=repeated_enrolments_distinct.values_list('pk', flat=True))

                    #results[j]['Enrolments'] = period_enrolments
                    #results[j]['Repeated Enrolments'] = repeated_enrolments

                    previous_result = StudentResult.objects.get(
                        student_registration=student_registrations[j-1])

                    data.update(
                        period_enrolments.get_statistics(
                            credits='registered_credits',
                            points='scored_points').items() +
                        period_enrolments.passed().get_statistics(
                            credits='passed_credits',
                            points='passed_points').items() +
                        repeated_enrolments.get_statistics(
                            credits='repeated_credits',
                            points='repeated_points').items()
                    )
                    try:
                        data.update({
                            'GPA':
                            round(data['scored_points'] /
                                  data['registered_credits'], 2)
                        })
                    except ZeroDivisionError:
                        data.update({
                            'GPA': 0.0
                        })
                    data.update({
                        'cumulative_scored_points': data['scored_points'] +
                        previous_result.cumulative_scored_points -
                        data['repeated_points'],
                        'cumulative_registered_credits':
                        data['registered_credits'] +
                        previous_result.cumulative_registered_credits -
                        data['repeated_credits'],
                        'cumulative_passed_credits':
                        data['passed_credits'] +
                        previous_result.cumulative_passed_credits
                    })
                    try:
                        data.update({
                            'cumulative_GPA':
                            round(data['cumulative_scored_points'] /
                                  data['cumulative_registered_credits'], 2)
                        })
                    except ZeroDivisionError:
                        data.update({
                            'cumulative_GPA': 0.0
                        })
                    self.__update_results(i, data)

            j += 1


#    def remaining_courses(self, passed_courses, DegreeCourse):
        #return DegreeCourse.objects.exclude(course=self.passed_courses())

    #def possilbke_wto_enroll(self):
     #   return

    def get_enroled_courses(self):

        return StudentEnrolment.objects.filter(student_registration__student=self).enroled()

    def get_passed_courses(self):

        return StudentEnrolment.objects.filter(student_registration__student=self).passed()

    def get_failed_courses(self):

        return StudentEnrolment.objects.filter(student_registration__student=self).failed()

    def get_degree(self):

        return self.studentregistration.last().degrees.all()[0]

    def get_remaining_courses(self):
        """"""

        return self.studentregistration.last().degrees.all()[0].\
            courses.all().exclude(
            code__in=self.get_passed_courses().values_list(
                'code', flat=True)
        )

    def get_enrolment_restriction(self):

        #we first
        # first_filter = CourseCatalogue.objects.exclude(pk=self.get_passed_courses()
        # )
        requirements = [course for course in self.get_remaining_courses()
                        if course.required_for.all()
                    ]

        #the below is just magic :)
        prerequisites_restriction = [
            course for sub in [
                requirement.required_for.all() for requirement in
                requirements if requirement not in self.get_passed_courses()
            ] for course in sub]

        #magic isn't explained but here I go:
        # we already got a list of courses which are required for other course
        # and we called that...drum-roll...requirements!!
        # now we get what courses depend on these requirements with:
        # requirement.required_for.all() <--- we do that for each reqs
        # then we check if the requirement is one of the passed_courses
        # if it's NOT PASSED, we add the required_for.all() in a list

        level_restriction = []
        if self.get_remaining_courses().filter(level=100).exists():
            level_restriction.append(300)
        if self.get_remaining_courses().filter(level=200).exists():
            level_restriction.append(400)
        if self.get_remaining_courses().filter(level=300).exists():
            level_restriction.append(500)

        prereqs_restriction = [course.code for course in list(dict.fromkeys(prerequisites_restriction))]
        restriction = dict(
        [('Prerequisites Restriction', self.get_remaining_courses().filter(
            code__in=prereqs_restriction)),
         ('Level Restriction', self.get_remaining_courses().filter(
             level__in=level_restriction))]
        )

        return restriction

    def get_period_course_restriction(self):
        """"""
        pass

    def get_progress(self):
        results = self.get_prettier_results()[0]
        degree = self.get_degree()
        courses = self.get_degree().courses.all()
        degree_progress = dict([(str(degree), {})])
        degree_progress[str(degree)].update({'Courses': []})
        degree_progress[str(degree)].update({'Statistics': {}})

        progress = degree_progress[str(degree)]

        for course in courses:
            if (
                self.get_passed_courses().filter(
                    code=course.code).exists() or
                    self.get_passed_courses().filter(
                        course__in=course.equalled_courses.all())):
                progress['Courses'].append({
                    'code': course.code, 'name_en': course.name_en,
                    'credit': course.credit, 'status': 'Passed'})
            elif self.get_failed_courses().filter(code=course.code).exists():
                progress['Courses'].append({
                    'code': course.code, 'name_en': course.name_en,
                    'credit': course.credit, 'status': 'Failed'})
            elif self.get_enroled_courses().filter(
            code=course.code, grade=None).exists():
                progress['Courses'].append({
                    'code': course.code, 'name_en': course.name_en,
                    'credit': course.credit,
                    'status': 'No grade'})
            elif (self.get_enrolment_restriction(
            )['Prerequisites Restriction'].filter(
            code=course.code).exists() or self.get_enrolment_restriction(
            )['Level Restriction'].filter(
            code=course.code).exists()):
                progress['Courses'].append({
                    'code': course.code, 'name_en': course.name_en,
                    'credit': course.credit,
                    'status': 'Restricted'})
            else:
                progress['Courses'].append({
                    'code': course.code, 'name_en': course.name_en,
                    'credit': course.credit,
                    'status': 'Possible to Enroll'})

        # for i in results['Periods']:
        cumulative_GPAs = [results['Results'][i]['Statistics']['cumulative_GPA'] for i in results['Periods']]
        period_GPAs = [results['Results'][i]['Statistics']['GPA'] for i in results['Periods']]
        periods = results['Periods']
        last_period = results['Periods'][-1]

        actual_period_count = results['Results'][last_period]['Statistics']['actual_period_count']
        completed_credits = courses.filter(
            code__in=self.get_passed_courses().values_list(
                'code', flat=True)).aggregate(Sum('credit')).values()[0]
        required_credits = courses.aggregate(Sum('credit')).values()[0]
        average_performance = completed_credits/float(actual_period_count)
        estimated_number_of_periods = int(required_credits/average_performance)
        completion_percentage = int(100*completed_credits/required_credits)

        progress['Statistics'].update(
            {'GPA': period_GPAs,
             'cumulative_GPA': cumulative_GPAs,
             'actual_period_count': actual_period_count,
             'completed_credits': completed_credits,
             'required_credits': required_credits,
             'average_performance': average_performance,
             'estimated_number_of_periods': estimated_number_of_periods,
             'periods': periods,
             'completion_percentage': completion_percentage
         })

        return [degree_progress]

        #return not_possible_to_enrol

    # def get_absolute_url(self):
    #     return reverse('student-home',
    #                    kwargs={
    #                        'registration_number': self.registration_number,
    #                    }
    #     )

    class Meta:
        app_label = 'UIS'


class StudentRegistration(UISBaseModel):
    """
    this describes the m2m relation between a student and terms

    TODO: maybe the student registration statuses need to be reviewed!

    random thoughts:

    - registered and suspended students are easy to deal with, but what about
      'dropped' students. Certainly they won't say this term we are dropping
      (i.e. we are not going to register nor are we going to suspend studying).
      the solution is: run something like a cron job to add 'dropped' status to
      all students who didn't register/suspend after a period of time!

    - on 3:15 (a.m.), 16/05/15, i moved most things that i thought should belong
      to studentregistration to student degree. I think this bests model
      multiple degrees. I don't know why I'm obsessed by multiple degrees.
      it won't happen in the near feature in our ****** universities.

    - on 2:10 (p.m.) 19/05/15, room K106, I just undo the things I did above.
      thinking about multiple degrees is premature!
    """

    student_registration_id = models.UUIDField(primary_key=True,
                                               default=uuid.uuid4,
                                               editable=False)


    student = models.ForeignKey('Student', verbose_name=_('student'),
                                related_name='studentregistration')
    # period = models.ForeignKey('Period', verbose_name=_('period'),
    #                            related_name='studentregistration')
    # suspension_type = models.CharField(
    #     max_length=1, choices=SUSPENSION_TYPE, default=NORMAL)
    DISCIPLINARY = 'DS'
    EXCEPTION = 'ES'
    NORMAL = 'NS'
    SUSPENSION_TYPE = (
        (DISCIPLINARY, _('Disciplinary Suspension ')),
        (EXCEPTION, _('Exceptional Suspension')),
        (NORMAL, _('Normal Suspension')),
    )
    REGISTERED = 'R'
    #SUSPENDED = 'S'
    DROPPED = 'D' # منطقع
    REGISTRATION_NOT_COMPLETED = 'RNC'
    REGISTRATION_TYPE = (
        (_('Suspended'), SUSPENSION_TYPE),
        (REGISTERED, _('Registered')),
        (DROPPED, _('Dropped Out')),
        (REGISTRATION_NOT_COMPLETED, _('Registration not completed')),
    )

    registration_type = models.CharField(
        max_length=3, choices=REGISTRATION_TYPE,
        default=REGISTRATION_NOT_COMPLETED)

    period_degree = models.ForeignKey('PeriodDegree')

    enrolments = models.ManyToManyField('Section',
                                        through='StudentEnrolment', blank=True)
    # enrolments = models.ManyToManyField('Section',
    #                                     through='StudentEnrolment', blank=True)

    class Meta:
        app_label = 'UIS'
        unique_together = (
            ('student', 'period_degree'),
        )
        ordering = (
            ('student', 'period_degree__period')
        )

    def __unicode__(self):
        return unicode(self.student)


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
        unique_together = ('student_registration', 'section', 'grade')

    def __unicode__(self):
        return (unicode(self.student_registration) + ' '
                + str(self.section) + str(self.grade))

    def save(self, *args, **kwargs):
        if self.grade is None:
            if (self.carry_marks is None and self.final_exam is None):
                pass
            elif (self.carry_marks is None or self.final_exam is None):
                raise IntegrityError
            else:
                self.grade = float(self.carry_marks) + float(self.final_exam)
        elif self.grade is not None and (self.carry_marks is not None or self.final_exam is not None):
            raise IntegrityError

        super(StudentEnrolment, self).save(*args, **kwargs)

        # Call the "real" save()

'''
THE PARAGRAPH BELOW TRIES TO EXPLAIN MY THOUGHTS

I WILL HAVE A STUDENT_DEGREE TABLE/MODEL WHICH WILL STORE ALL TYPES OF GRADES

THEN DEPENDING ON THE ENROLMENT_STATUS (WHICH IS A FIELD IN THE STUDENT_ENROLMENT

TABLE), THE GRADE IN THE STUDENT_ENROLMENT WILL BE SET, FOR EXAMPLE, IF IT IS

"CREDITS WITHELD", THE STUDENT_ENROLMENT GRADE WILL BE NULL EVEN THOUGH IN THE

STUDENT GRADE TABLE, IT'S VALUE WILL NOT BE NULL!

THE STUDENT GRADE TABLE WILL ALSO HOLD CHANGES TO GRADES.
'''

# class StudentGrade(UISBaseModel):

#     student_grade_id = models.UUIDField(primary_key=True,
#                                         default=uuid.uuid4,
#                                         editable=False)

#     student_enrolment = models.ForeignKey('StudentEnrolment',
#                                           on_delete=models.PROTECT)

#     grade = models.FloatField(validators=[validate_grade])


# class StudentGradeChange(UISBaseModel):

#     student_grade_change_id = models.UUIDField(primary_key=True,
#                                                default=uuid.uuid4,
#                                                editable=False)

#     original_student_grade = models.ForeignKey('StudentGrade',
#                                                on_delete=models.PROTECT)

#     new_grade = models.FloatField(validators=[validate_grade])



# class StudentDegree(models.Model):

#     """
#     m2m between studentREGISTRATION and period_degrees
#     """

#     student_registration = models.ForeignKey('StudentRegistration',
#                                              related_name='studentdegree')
#     period_degree = models.ForeignKey('PeriodDegree',
#                                       on_delete=models.PROTECT,
#                                       related_name='studentdegree')

#     class Meta:
#         app_label = 'UIS'
#         unique_together = ('student_registration', 'period_degree')

#     def __unicode__(self):
#         return unicode(self.student_registration) + ' ' + str(self.degree)
class StudentResult(models.Model):
    '''
    THIS SHOULD BE A MATERIALIZED VIEW, I DON'T LIKE THE CURRENT IMPLEMENTATION.
    '''

    student_results_id =  models.UUIDField(primary_key=True,
                                           default=uuid.uuid4,
                                           editable=False)

    student_registration = models.OneToOneField('StudentRegistration')


    period_count = models.IntegerField()
    actual_period_count = models.IntegerField()

    registered_credits = models.FloatField()
    passed_credits = models.FloatField()
    repeated_credits = models.FloatField()
    cumulative_registered_credits = models.FloatField()
    cumulative_passed_credits = models.FloatField()

    scored_points = models.FloatField()
    passed_points = models.FloatField()
    repeated_points = models.FloatField()
    cumulative_scored_points = models.FloatField()

    GPA = models.FloatField()
    cumulative_GPA = models.FloatField()


    class Meta:
        app_label = 'UIS'
        ordering = (
            'student_registration',
        )

        #         unique_together = ('student_registration', 'period_degree')
