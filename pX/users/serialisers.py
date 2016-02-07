# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers

from ..users.models import Employee, Person


class PersonSerialiser(serializers.HyperlinkedModelSerializer):

    full_name_ar = serializers.CharField(source='full_name_ar')
    full_name = serializers.CharField(source='full_name')

    class Meta:
        model = Person
        fields = ('url', 'first_name_ar', 'last_name_ar',
                  'first_name', 'last_name',
                  'full_name_ar', 'full_name')


class EmployeeSerialiser(PersonSerialiser):

    # student = serializers.HyperlinkedIdentityField(
    #     view_name='student-detail',
    #     lookup_field='student.registration_number',
    # )

    class Meta:
        model = Employee
        # fields = ('student',)



# from rest_framework import serializers
# from UIS.models.users import UISUser, Person, UserProfile, Employee
# from UIS.models.students import (Student, StudentEnrolment,
#                                  StudentResult, StudentRegistration)
# from UIS.models.courses import Section, PeriodCourse, Course
# from UIS.models.time_period import Period, PeriodDegree

# class UserSerialiser(serializers.HyperlinkedModelSerializer):

#     class Meta:
#         model = UISUser
#         fimetaelds = ('url', 'email')
#         # extra_kwargs = {
#         #     'url': {'lookup_field': 'email'}
#         #}
#         lookup_field = 'email'


# class ProfileRelatedField(serializers.RelatedField):
#     """
#     A custom field to use for the `profile` generic relationship.
#     """

#     def to_representation(self, value):
#         """
#         Serialize bookmark instances using a bookmark serializer,
#         and note instances using a note serializer.
#         """
#         context = {'request': self.context.get('request')}
#         if isinstance(value, Student):
#             serializer = StudentSerialiser(value, context=context)
#         elif isinstance(value, Employee):
#             serializer = EmployeeSerialiser(value, context=context)
#         else:
#             raise Exception('Unexpected type of tagged object')

#         return serializer.data




# class UserSerialiser(serializers.HyperlinkedModelSerializer):

#     profile_type = serializers.StringRelatedField(read_only=True)
#     person_id = serializers.UUIDField(source='profile.person_id')
#     # profile_id = serializers.PrimaryKeyRelatedField(read_only=True)

#     class Meta:
#         model = UserProfile
#         fields = ('profile_type', 'profile_id', 'person_id')



# class StudentRegistrationSerialiser(serializers.ModelSerializer):

#     period = serializers.StringRelatedField(source='period_degree.period')

#     class Meta:
#         model = StudentRegistration
#         exclude = ('student', )