from django.conf.urls import url, include
from UIS.views import *
from django.contrib.auth import views as auth_views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    # url(
    #     r'login/$', auth_views.login,
    #     {'template_name': 'UIS/login.html'},
    #     name='login'
    # ),

    # url(
    #     r'student/(?P<registration_number>[0-9]+?)/results/(?P<period>[0-3])' +
    #     r'/(?P<academic_year>[0-9]+?-[0-9]+?)/$',
    #     PeriodResultsView.as_view(), name='period-results'
    # ),
    # url(
    #     r'student/(?P<registration_number>[0-9]+?)/progress/$',
    #     StudentProgressView.as_view(), name='student-progress'
    # ),
    # url(
    #     r'student/(?P<registration_number>[0-9]+?)/enrol/(?P<period>[1-3])' +
    #     r'/(?P<academic_year>[0-9]+?-[0-9]+?)/$',
    #     AddEnrolmentView.as_view(), name='enrol'
    # ),
    # url(
    #     r'(?P<registration_number>[0-9]+)/enrol/(?P<period>[1-3])' +
    #     r'/(?P<academic_year>[0-9]+?-[0-9]+?)/delete/(?P<course_code>\w+?)/$',
    #     DeleteEnrolmentView.as_view(), name='delete_enrolment'
    # ),
    # url(
    #     r'student/(?P<registration_number>[0-9]+?)/$',
    #     StudentHomeView.as_view(), name='student-home'
    # ),
    # url(
    #     r'employee/(?P<username>[\w.@+-]+?)/$',
    #     EmployeeHomeView.as_view(), name='employee-home'
    # ),
    # url(
    #     r'^$', LoginRedirectView.as_view(), name='login-redirect'
    # ),

]
