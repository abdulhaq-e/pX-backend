from django.core.signals import m2m_changed
from django.dispatch import receiver
from django.utils import IntegrityError
from UIS.models.courses import CourseCatalogue


@receiver(m2m_changed, sender=CourseCatalogue.prerequisites.through)
def verify_course_catalogue_uniqueness(sender, **kwargs):
    course = kwargs.get('instance', None)
    action = kwargs.get('action', None)
    prerequisites = kwargs.get('pk_set', None)

    if action == 'pre_add':
        if (course.prerequisites.all().exclude(
                pk__in=CourseCatalogue.objects.filter(
                    pk__in=prerequisites).exists()) and
            CourseCatalogue.objects.filter(code=course.code,
                                           name=course.name,
                                           is_compulsary=course.is_compulsary,
                                           is_obsolete=course.is_obsolete,
                                           department=course.department,
                                           credit=course.credit).count()>1):

            raise IntegrityError(
                    'Course %s already exists' % (course.name,)
            )
