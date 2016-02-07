# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import viewsets

from .models import SectionEnrolment
from ..serialisers.student_enrolment import SectionEnrolmentSerialiser
from ..filters.student_enrolment import SectionEnrolmentFilter


class SectionEnrolmentViewSet(viewsets.ModelViewSet):

    model = SectionEnrolment
    serializer_class = SectionEnrolmentSerialiser
    # queryset = SectionEnrolment.original.all()
    filter_class = SectionEnrolmentFilter

    def get_queryset(self):
        """
        """
        return SectionEnrolment.objects.select_related(
            'section__section_type__period_course__course').all()
    #     params = get_filter_params(self.request)
    #     student = params.get('student', None)
    #     registration_number = params.get('registration_number', None)
    #     # period = Period.objects.get(period=2, academic_year='2014,2015')
    #     # print period
    #     queryset = SectionEnrolment.original.all()
    #     if (student is not None):
    #         queryset = SectionEnrolment.original.filter(
    #             student_registration__student=student)
    #         return queryset
    #     elif (registration_number is not None):
    #         queryset = queryset.filter(
    #             student_registration__student__registration_number=registration_number)
    #     print queryset.query
    #     return queryset
        # # else:
        # queryset = SectionEnrolment.original.filter(
        #     student_registration__period_degree__period=period)
        # return queryset

        #     return SectionEnrolment.objects.all()
