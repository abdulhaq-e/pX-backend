from django.db.models.signals import m2m_changed, pre_save
from django.dispatch import receiver
from django.db import IntegrityError
from UIS.models.courses import Course
from UIS.models.students import StudentEnrolment


# @receiver(m2m_changed, sender=Course.prerequisites.through)
# def verify_course_catalogue_uniqueness(sender, **kwargs):
#     course = kwargs.get('instance', None)
#     action = kwargs.get('action', None)
#     prerequisites = kwargs.get('pk_set', None)

#     if action == 'pre_add':
#         if (course.prerequisites.all().exclude(
#                 pk__in=Course.objects.filter(
#                     pk__in=prerequisites).exists()) and
#             Course.objects.filter(code=course.code,
#                                   name=course.name,
#                                   is_compulsary=course.is_compulsary,
#                                   is_obsolete=course.is_obsolete,
#                                   department=course.department,
#                                   credit=course.credit).count()>1):

#             raise IntegrityError(
#                 'Course %s already exists' % (course.name,)
#             )


# @receiver(pre_save, sender=StudentEnrolment)
# def save_grade(sender, **kwargs):
#     enrolment = kwargs.get('instance', None)

#     if enrolment.carry_marks == '':
#         enrolment.carry_marks = None
#     if enrolment.final_exam == '':
#         enrolment.final_exam = None
#     if enrolment.grade == '':
#         enrolment.grade = None

#     if enrolment.grade is None:
#         # everything is null, i.e. an empty enrolment
#         if (enrolment.carry_marks is None and enrolment.final_exam is None):
#             pass
#         # if one of them is none, we have a problem, FIXME
#         elif (enrolment.carry_marks is None or enrolment.final_exam is None):
#             raise IntegrityError
#         else:
#             enrolment.grade = float(enrolment.carry_marks) + float(enrolment.final_exam)
#     # similarly, we can't have the total grade AND one of the other two
#     elif enrolment.grade is not None and (enrolment.carry_marks is not None or enrolment.final_exam is not None):
#         raise IntegrityError
