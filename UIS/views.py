from django.shortcuts import get_object_or_404
from django.views.generic import (DetailView, TemplateView,
                                  FormView, CreateView,
                                  DeleteView)
from django.views.generic.base import RedirectView
from django.core.urlresolvers import reverse
from models import *
from querysets import *
from forms import *
# from UIS.mixins import PeriodMixin, StudentMixin
# from extra_views import ModelFormSetView
# from braces.views import LoginRequiredMixin
from rest_framework import viewsets
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response
from rest_framework import status
import django_filters

from UIS.serialisers import (StudentSerialiser, UserSerialiser,
                             StudentEnrolmentSerialiser,
                             StudentResultSerialiser,
                             PeriodCourseSectionSerialiser,
                             SectionSerialiser)


class StudentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

#    lookup_field = 'registration_number'
    queryset = Student.objects.all()
    serializer_class = StudentSerialiser

    @detail_route()
    def get_results(self, request, pk=None):
        student = self.get_object()
        return Response(student.get_prettier_results())

    @detail_route()
    def get_progress(self, request, pk=None):
        student = self.get_object()
        return Response(student.get_progress())

    @detail_route()
    def get_enrolments(self, request, pk=None):
        student = self.get_object()
        enrolments = StudentEnrolment.objects.filter(
            student_registration__student=student)
        serialiser = EnrolmentSerialiser(enrolments, many=True)
        return Response(serialiser.data)

    @detail_route(methods=['post'])
    def enrol(self, request, pk=None):
        student = self.get_object()
        # section = Section.objects.get(
        #     section_id=request.data['section_id'])
        # #student_registration = request.data['student_registration']
        # request.data.pop('section_id')
        # request.data.update({'section': section})
        serialiser = EnrolmentSerialiser(data=request.data)

        if serialiser.is_valid():
            serialiser.save()
            # StudentEnrolment.objects.create(
            #     student_registration=serialiser.data['student_registration'],
            #     section=serialiser.data['section'])
            return Response({'status': 'enrolment added'})
        else:
            return Response(serialiser.errors,
                            status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):

    serializer_class = UserSerialiser
    queryset = UISUser.objects.all()


# class StudentEnrolmentFilter(django_filters.FilterSet):

#     registration_number = django_filters.CharFilter(
#         name="student_registration__student__registration_number")

#     class Meta:
#         model = StudentEnrolment
#         fields = ('registration_number',)


class StudentEnrolmentViewSet(viewsets.ModelViewSet):

    model = StudentEnrolment
    serializer_class = StudentEnrolmentSerialiser
    # filter_class = StudentEnrolmentFilter

    def get_queryset(self):
        """
        """
        student = self.request.QUERY_PARAMS.get(
            'student_id', None)
        registration_number = self.request.QUERY_PARAMS.get(
            'registration_number', None)
        period = Period.objects.get(period=2, academic_year='2014,2015')
        print period
        if (student is not None):
            queryset = StudentEnrolment.original.filter(
                student_registration__student=student,
                student_registration__period_degree__period=period)
            return queryset
        elif (registration_number is not None):
            queryset = StudentEnrolment.original.filter(
                student_registration__student__registration_number=registration_number,
                student_registration__period_degree__period=period)
            return queryset
        # else:
        #     return StudentEnrolment.objects.all()


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

class SectionViewSet(viewsets.ModelViewSet):
    model = Section
    serializer_class = SectionSerialiser
    #queryset = Section.objects.all()

    def get_queryset(self):
        """
        """
        period = self.request.QUERY_PARAMS.get(
            'period', None)

        if (period is not None):
            queryset = Section.objects.filter(
                period_course__period=period)
        else:
            return Section.objects.all()
        return queryset


# class PeriodCourseFilter(django_filters.FilterSet):

#     class Meta:
#         model = PeriodCourse
#         fields = ('period',)


# class PeriodCourseViewSet(viewsets.ModelViewSet):

#     model = PeriodCourse
#     serializer_class = PeriodCourseSerialiser
#     filter_class = PeriodCourseFilter

#     def get_queryset(self):
#         """
#         """
#         queryset = PeriodCourse.objects.all()
#         student_registration = self.request.QUERY_PARAMS.get(
#             'student_registration', None)
#         restricted = self.request.QUERY_PARAMS.get('restricted', False)
#         if (student_registration is not None):
#             period = StudentRegistration.objects.get(
#                 id=student_registration).period
#             if not restricted:
#                 queryset = queryset.filter(period=period)
#         return queryset
