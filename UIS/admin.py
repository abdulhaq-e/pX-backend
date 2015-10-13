from django.contrib import admin
from UIS.models import *

# # Register your models here.

# class StudentAdmin(admin.ModelAdmin):
#     fieldsets = [
#         ('Student Identification', {'fields': ['student', 'first_name_ar',
#                                                 'last_name_ar', 'first_name_en',
#                                                 'last_name_en', 'gender','date_of_birth',
#                                                'nationality', 'address']}),
#         ('Academic Details', {'fields': ['status', 'advisor', 'degree']})
#     ]
#     #filter_horizontal = ('degree',)


# class PerioCourseInline(admin.TabularInline):
#     model = PeriodCourse


# class DegreeCourseInline(admin.TabularInline):
#     model = DegreeCourse


# class SectionInstructorInline(admin.TabularInline):
#     model = SectionInstructor
#     extra = 2


# # class TimeTableInline(admin.TabularInline):
# #     model = TimeTable
# #     extra = 2


# # class SectionAdmin(admin.ModelAdmin):
# #     inlines = (SectionInstructorInline, TimeTableInline)


# class DegreeAdmin(admin.ModelAdmin):
#     inlines = (DegreeCourseInline,)

# class CourseAdmin(admin.ModelAdmin):
#     filter_horizontal = ('prerequisites', 'equalled_courses')
# # #     inlines = (TermCourseInline, DegreeCourseInline)


# # class TermAdmin(admin.ModelAdmin):
# #     inlines = (TermCourseInline,)


# class TimeSlotAdmin(admin.ModelAdmin):
#     pass


# class StudentEnrolmentAdmin(admin.ModelAdmin):
#     list_display = ('student', 'section', 'grade')
#     list_filter = ('student',)

# #class FacilityReservationAdmin(admin.ModelAdmin):
#  #   pass

# #admin.site.register(FacilityReservation, FacilityReservationAdmin)

# #admin.site.register(TimeTable)
# #admin.site.register(TimeSlot)#, TimeSlotAdmin)
# admin.site.register(StudentEnrolment)
# admin.site.register(Student)#, StudentAdmin)
# admin.site.register(Department)
# admin.site.register(Faculty)
# admin.site.register(Course, CourseAdmin)
# # # admin.site.register(Course)#, CourseAdmin)
# admin.site.register(Degree)
# admin.site.register(Employee)
# # # #admin.site.register(Advisor)
# admin.site.register(Section)#, SectionAdmin)
# # #admin.site.register(DegreeCourse)
# # admin.site.register(AcademicYear)
# # admin.site.register(Term)#, TermAdmin)
# # admin.site.register(Period)#, TermAdmin)
# ##admin.site.register(TermCourse)
# #admin.site.register(Facility)
