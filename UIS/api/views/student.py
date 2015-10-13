# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import viewsets

from UIS.models.students import Student
from ..serialisers.student import StudentSerialiser
from ..filters.student import StudentFilter


class StudentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    #renderer_classes = (JsonApiRenderer, )
    queryset = Student.objects.all()
    serializer_class = StudentSerialiser
    filter_class = StudentFilter

    # def get_queryset(self):
    #     """
    #     """
    #     params = get_filter_params(self.request)
    #     student = params.get('student', None)
    #     registration_number = params.get('registration_number', None)
    #     # period = Period.objects.get(period=2, academic_year='2014,2015')
    #     # print period
    #     queryset = Student.objects.all()
    #     if (student is not None):
    #         queryset = queryset.filter(pk=student)
    #     elif (registration_number is not None):
    #         queryset = queryset.filter(
    #             registration_number=registration_number)
    #     print queryset.query
    #     return queryset

    #    lookup_field = 'registration_number'
    # @detail_route()
    # def get_results(self, request, pk=None):
    #     student = self.get_object()
    #     return Response(student.get_prettier_results())

    # @detail_route()
    # def get_progress(self, request, pk=None):
    #     student = self.get_object()
    #     return Response(student.get_progress())

    # @detail_route()
    # def get_enrolments(self, request, pk=None):
    #     student = self.get_object()
    #     enrolments = StudentEnrolment.objects.filter(
    #         student_registration__student=student)
    #     serialiser = EnrolmentSerialiser(enrolments, many=True)
    #     return Response(serialiser.data)

    # @detail_route(methods=['post'])
    # def enrol(self, request, pk=None):
    #     student = self.get_object()
    #     # section = Section.objects.get(
    #     #     section_id=request.data['section_id'])
    #     # #student_registration = request.data['student_registration']
    #     # request.data.pop('section_id')
    #     # request.data.update({'section': section})
    #     serialiser = EnrolmentSerialiser(data=request.data)

    #     if serialiser.is_valid():
    #         serialiser.save()
    #         # StudentEnrolment.objects.create(
    #         #     student_registration=serialiser.data['student_registration'],
    #         #     section=serialiser.data['section'])
    #         return Response({'status': 'enrolment added'})
    #     else:
    #         return Response(serialiser.errors,
    #                         status=status.HTTP_400_BAD_REQUEST)
