# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import viewsets

from UIS.models.students import StudentResult
from ..serialisers.student_result import StudentResultSerialiser


class StudentResultViewSet(viewsets.ReadOnlyModelViewSet):

    model = StudentResult
    serializer_class = StudentResultSerialiser
    # filter_class = StudentEnrolmentFilter

    def get_queryset(self):
        """
        """
        student = self.request.QUERY_PARAMS.get(
            'student_id', None)
        registration_number = self.request.QUERY_PARAMS.get(
            'registration_number', None)
        if (student is not None):
            return StudentResult.objects.filter(
                student_registration__student=student)# __student__registration_number=registration_number)
        elif registration_number is not None:
            return StudentResult.objects.filter(
                student_registration__student__registration_number=registration_number)
        else:
            return StudentResult.objects.all()
