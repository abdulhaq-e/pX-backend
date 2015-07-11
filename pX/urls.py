from django.conf.urls import include, url
from django.views.generic import TemplateView
from rest_framework import routers
from django.contrib import admin
from UIS.views import (StudentViewSet, UserViewSet,
#                       PeriodCourseViewSet,
                       StudentResultViewSet,
                       StudentEnrolmentViewSet,
                       SectionViewSet)

router = routers.DefaultRouter()
#router.register(r'users', UserViewSet)
router.register(r'students',
                StudentViewSet)
router.register(r'users',
                UserViewSet)
# router.register(r'period_courses',
#                 PeriodCourseViewSet,
#                 base_name='period_course')
router.register(r'enrolments',
                StudentEnrolmentViewSet,
                base_name='enrolment')
router.register(r'results',
                StudentResultViewSet,
                base_name='result')
router.register(r'sections',
                SectionViewSet,
                base_name='section')

urlpatterns = [

    url(r'^api/v1/', include(router.urls)
    ),

    url(
        r'^api-auth/',
        include('rest_framework.urls',
                namespace='rest_framework')
    ),

    url(r'^api/v1/auth/login/', 'rest_framework_jwt.views.obtain_jwt_token'),

    url(
        r'^docs/', include('rest_framework_swagger.urls')
    ),

    # url('', include('django.contrib.auth.urls')),

    # url(
    #     r'^$', 'pX.views.main'
    # ),

    url(
         r'^admin/', include(admin.site.urls)
    ),
    # url(
    #     r'^user/', include('UIS.urls', namespace='UIS')
    # )
           ]
