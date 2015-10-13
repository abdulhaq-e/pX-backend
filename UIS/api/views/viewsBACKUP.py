# from django.shortcuts import get_object_or_404
# from django.views.generic import (DetailView, TemplateView,
#                                   FormView, CreateView,
#                                   DeleteView)
# from django.views.generic.base import RedirectView
# from django.core.urlresolvers import reverse
# from models import *
# from querysets import *
# from forms import *
# # from UIS.mixins import PeriodMixin, StudentMixin
# # from extra_views import ModelFormSetView
# # from braces.views import LoginRequiredMixin

# from rest_framework.decorators import detail_route, list_route
# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework.renderers import JSONRenderer


# from UIS.serialisers import (StudentSerialiser,
#                              UserSerialiser,
#                              PeriodDegreeSerialiser,
#                              CourseSerialiser,
#                              StudentRegistrationSerialiser,
#                              StudentEnrolmentSerialiser,
#                              StudentResultSerialiser,
#                              PeriodCourseSectionSerialiser,
#                              SectionSerialiser)
# from UIS.utils import get_filter_params











#     # def get_queryset(self):
#     #     """
#     #     """
#     #     period = self.request.QUERY_PARAMS.get(
#     #         'period', None)

#     #     if (period is not None):
#     #         queryset = Section.objects.filter(
#     #             period_course__period=period)
#     #     else:
#     #         return Section.objects.all()
#     #     return queryset




# # class PeriodCourseFilter(django_filters.FilterSet):

# #     class Meta:
# #         model = PeriodCourse
# #         fields = ('period',)


# # class PeriodCourseViewSet(viewsets.ModelViewSet):

# #     model = PeriodCourse
# #     serializer_class = PeriodCourseSerialiser
# #     filter_class = PeriodCourseFilter

# #     def get_queryset(self):
# #         """
# #         """
# #         queryset = PeriodCourse.objects.all()
# #         student_registration = self.request.QUERY_PARAMS.get(
# #             'student_registration', None)
# #         restricted = self.request.QUERY_PARAMS.get('restricted', False)
# #         if (student_registration is not None):
# #             period = StudentRegistration.objects.get(
# #                 id=student_registration).period
# #             if not restricted:
# #                 queryset = queryset.filter(period=period)
# #         return queryset
