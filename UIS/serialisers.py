from rest_framework import serializers
from UIS.models.users import UISUser, Person, UserProfile, Employee
from UIS.models.students import (Student, StudentEnrolment,
                                 StudentResult, StudentRegistration)
from UIS.models.courses import Section, PeriodCourse, CourseCatalogue
from UIS.models.time_period import Period

# class UserSerialiser(serializers.HyperlinkedModelSerializer):

#     class Meta:
#         model = UISUser
#         fimetaelds = ('url', 'email')
#         # extra_kwargs = {
#         #     'url': {'lookup_field': 'email'}
#         #}
#         lookup_field = 'email'


class StudentSerialiser(serializers.ModelSerializer):

    #first_name = serializers.CharField(source='person_ptr.first_name')
    # url = serializers.HyperlinkedIdentityField(
    #     lookup_field='registration_number',
    #     view_name='student-detail'
    # )
    student_registrations = serializers.PrimaryKeyRelatedField(
        source='studentregistration', read_only=True, many=True)
    # periods = serializers.PrimaryKeyRelatedField(
    #     source='periods.student_read_only=True, many=True)

    full_name_ar = serializers.CharField(source='get_full_name_ar')
    full_name = serializers.CharField(source='get_full_name')

    class Meta:
        model = Student

        exclude = ('details', 'periods')
        #fields += ('url',)# 'first_name_ar', 'last_name_ar',
                  #'first_name', 'last_name', 'registration_number',)

        # extra_kwargs = {
        #     'url': {'lookup_field': 'registration_number'}
        # }


class EmployeeSerialiser(serializers.ModelSerializer):

    # student = serializers.HyperlinkedIdentityField(
    #     view_name='student-detail',
    #     lookup_field='student.registration_number',
    # )

    full_name_ar = serializers.CharField(source='get_full_name_ar')
    full_name = serializers.CharField(source='get_full_name')


    class Meta:
        model = Employee
        # fields = ('student',)


class PersonSerialiser(serializers.HyperlinkedModelSerializer):

    # student = serializers.HyperlinkedIdentityField(
    #     view_name='student-detail',
    #     lookup_field='student.registration_number',
    # )

    class Meta:
        model = Person
        # fields = ('student',)


class ProfileRelatedField(serializers.RelatedField):
    """
    A custom field to use for the `profile` generic relationship.
    """

    def to_representation(self, value):
        """
        Serialize bookmark instances using a bookmark serializer,
        and note instances using a note serializer.
        """
        if isinstance(value, Student):
            serializer = StudentSerialiser(value)
        elif isinstance(value, Employee):
            serializer = EmployeeSerialiser(value)
        else:
            raise Exception('Unexpected type of tagged object')

        return serializer.data


class UserSerialiser(serializers.ModelSerializer):

    profile = ProfileRelatedField(source='userprofile.profile',
                                  read_only=True)
    profile_type = serializers.CharField(source='userprofile.profile_type')
    roles = serializers.StringRelatedField(many=True)

    class Meta:
        model = UISUser
        exclude = ('password',)

# class UserSerialiser(serializers.HyperlinkedModelSerializer):

#     profile_type = serializers.StringRelatedField(read_only=True)
#     person_id = serializers.UUIDField(source='profile.person_id')
#     # profile_id = serializers.PrimaryKeyRelatedField(read_only=True)

#     class Meta:
#         model = UserProfile
#         fields = ('profile_type', 'profile_id', 'person_id')


class CourseSerialiser(serializers.ModelSerializer):

    class Meta:
        model = CourseCatalogue


class StudentEnrolmentSerialiser(serializers.ModelSerializer):

    course = CourseSerialiser(
        source='section.section_type.period_course.course'
    )
    # registration_number = serializers.StringRelatedField(
    #     source='student_registration.student.registration_number')

    class Meta:
        model = StudentEnrolment
        # exclude = ()
        #read_only_fields = ('section', 'student_registration')


class SectionSerialiser(serializers.ModelSerializer):

    class Meta:
        model = Section
        #exclude = ('period_course',)


class PeriodCourseSectionSerialiser(serializers.ModelSerializer):

    course = CourseSerialiser(read_only=True)
    main_section = SectionSerialiser(source='section_set', many=True)

    class Meta:
        model = PeriodCourse


class StudentRegistrationSerialiser(serializers.ModelSerializer):

    period = serializers.StringRelatedField(source='period_degree.period')

    class Meta:
        model = StudentRegistration
        exclude = ('student', )


class StudentResultSerialiser(serializers.ModelSerializer):

    student_registration = StudentRegistrationSerialiser()

    class Meta:
        model = StudentResult
