# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import viewsets

from UIS.models.students import StudentEnrolment
from ..serialisers.student_enrolment import StudentEnrolmentSerialiser
from ..filters.student_enrolment import StudentEnrolmentFilter


class StudentEnrolmentViewSet(viewsets.ModelViewSet):

    model = StudentEnrolment
    serializer_class = StudentEnrolmentSerialiser
    # queryset = StudentEnrolment.original.all()
    filter_class = StudentEnrolmentFilter

    def get_queryset(self):
        """
        """
        return StudentEnrolment.objects.select_related(
            'section__section_type__period_course__course').all()
    #     params = get_filter_params(self.request)
    #     student = params.get('student', None)
    #     registration_number = params.get('registration_number', None)
    #     # period = Period.objects.get(period=2, academic_year='2014,2015')
    #     # print period
    #     queryset = StudentEnrolment.original.all()
    #     if (student is not None):
    #         queryset = StudentEnrolment.original.filter(
    #             student_registration__student=student)
    #         return queryset
    #     elif (registration_number is not None):
    #         queryset = queryset.filter(
    #             student_registration__student__registration_number=registration_number)
    #     print queryset.query
    #     return queryset
        # # else:
        # queryset = StudentEnrolment.original.filter(
        #     student_registration__period_degree__period=period)
        # return queryset

        #     return StudentEnrolment.objects.all()
