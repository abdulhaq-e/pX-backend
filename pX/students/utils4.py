# # from .models import StudentResult
# # from .section_enrolments.models import SectionEnrolment


# def get_results(student):


    # def get_enroled_courses(self):

    #     return SectionEnrolment.objects.filter(
    #         period_registration__student=self).enroled()

    # def get_passed_courses(self):

    #     return SectionEnrolment.objects.filter(
    #         period_registration__student=self).passed()

    # def get_failed_courses(self):

    #     return SectionEnrolment.objects.filter(
    #         period_registration__student=self).failed()

    # def get_degree(self):
    #     """
    #     """
    #     return self.period_registrations.last().period_degree.degree

    # def get_remaining_courses(self):
    #     """
    #     """
    #     return (
    #         self.get_degree().courses.all().
    #         exclude(
    #             code__in=self.get_passed_courses().values_list(
    #                 'code', flat=True)).
    #         exclude(
    #             equalled_courses__code__in=self.get_passed_courses().
    #             values_list(
    #                 'code', flat=True)
    #         )
    #     )

    # def get_allowed_enrolments(self):

    #     #we first
    #     # first_filter = Course.objects.exclude(pk=self.get_passed_courses()
    #     # )
    #     self.allowed_enrolment.all().delete()

    #     autumn2011 = Period.objects.get(academic_year='2011,2012', period=1)
    #     post_autumn2011 = Period.objects.filter(
    #         period__gte=autumn2011.period,
    #         academic_year__gte=autumn2011.academic_year)

    #     if (
    #             self.period_registrations.first().period_degree.period not in
    #             post_autumn2011
    #     ):
    #         remaining_courses = self.get_remaining_courses().exclude(
    #             code='GS206')
    #     else:
    #         remaining_courses = self.get_remaining_courses()

    #     four_years_high_school = ['022855391', '022804126', '022071317',
    #                               '021714174', '021714386', '02106341']
    #     if self.registration_number in four_years_high_school:
    #         remaining_courses = remaining_courses.exclude(
    #             code__in=['GE127', 'GS115', 'GS115L', 'ME201', 'ME307'])

    #     if self.registration_number == '021120007':
    #         remaining_courses = remaining_courses.exclude(
    #             code__in=['GE125', 'GE127', 'GE129', 'GH141',
    #                       'GH150', 'GS101', 'GS115', 'GS111'])

    #     prerequisites_restriction = (
    #         CoursePrerequisite.objects.
    #         filter(
    #             course__in=remaining_courses
    #         ).exclude(
    #             prerequisite__code__in=self.get_passed_courses().values_list(
    #                 'code', flat=True)
    #         ).exclude(
    #             prerequisite__equalled_courses__code__in=self.get_passed_courses().values_list(
    #                 'code', flat=True)
    #         )
    #     )


    #     allowed_enrolments = remaining_courses.exclude(
    #         prerequisites__in=prerequisites_restriction)

    #     general_courses = ['GS101', 'GS102', 'GS203',
    #                        'GS204', 'GS111', 'GS112',
    #                        # 'GS112L',
    #                        'GS115',
    #                        # 'GS115L',
    #                        'GS200',
    #                        'GS206',
    #                        'GE121',
    #                        'GE125',
    #                        'GE127',
    #                        'GE129',
    #                        # 'GE129L',
    #                        'GE133',
    #                        'GE222',
    #                        'GH141',
    #                        'GH142',
    #                        'GH150',
    #                        'GH151',
    #                        # 'GH152'
    #     ]

    #     if (
    #             self.period_registrations.last().
    #             studentresult.cumulative_passed_credits < 120
    #     ) or (
    #         remaining_courses.filter(
    #             code__in=general_courses
    #         ).exists()
    #     ):
    #         allowed_enrolments = allowed_enrolments.exclude(code='AE599')

    #     excluded_from_regulations = ['GH152', 'GS112L',
    #                                  'GS115L', 'GE129L',
    #                                  'ME201', 'ME206',
    #                                  'ME215']

    #     elective = True
    #     if remaining_courses.exclude(
    #             code__in=excluded_from_regulations).filter(level=100).exists():
    #         allowed_enrolments = allowed_enrolments.exclude(
    #             level__in=[300, 400, 500])
    #         elective = False
    #     if remaining_courses.exclude(
    #             code__in=excluded_from_regulations).filter(level=200).exists():
    #         allowed_enrolments = allowed_enrolments.exclude(
    #             level__in=[400, 500])
    #         elective = False
    #     if remaining_courses.exclude(
    #             code__in=excluded_from_regulations).filter(level=300).exists():
    #         allowed_enrolments = allowed_enrolments.exclude(level=500)
    #         elective = False

    #     if (self.get_passed_courses().values_list(
    #             'code', flat=True).filter(code__startswith='AE555').count()
    #         >= 6):
    #         elective = False

    #     if elective:
    #         electives = Course.objects.filter(
    #             code__in=['AE555ADS', 'AE555EPM', 'AE555INS', 'AE555SMS']
    #         )
    #         possible_electives = electives.exclude(
    #             code__in=self.get_passed_courses().values_list(
    #                 'code', flat=True))
    #         for c in possible_electives:
    #             StudentAllowedEnrolment.objects.create(
    #                 student=self,
    #                 course=c)
    #         # self.allowed_enrolment.add(electives)

    #     #for course in allowed_enrolments:
    #     for c in allowed_enrolments:
    #         StudentAllowedEnrolment.objects.create(
    #                 student=self,
    #                 course=c)

    #     # self.allowed_enrolment.add(allowed_enrolments)

    #     return Course.objects.filter(
    #         studentallowedenrolment__in=self.allowed_enrolment.all()
    #     )

    # def get_max_enrolled_credits(self):

    #     return (
    #         21 if self.period_registrations.last().
    #         studentresult.cumulative_GPA > 75 else 18
    #     )

    #     # requirements = [course for course in self.get_remaining_courses()
    #     #                 if course.required_for.all()
    #     #             ]

    #     # #the below is just magic :)
    #     # prerequisites_restriction = [
    #     #     course for sub in [
    #     #         requirement.required_for.all() for requirement in
    #     #         requirements if requirement not in self.get_passed_courses()
    #     #     ] for course in sub]

    #     # #magic isn't explained but here I go:
    #     # # we already got a list of courses which are required for other course
    #     # # and we called that...drum-roll...requirements!!
    #     # # now we get what courses depend on these requirements with:
    #     # # requirement.required_for.all() <--- we do that for each reqs
    #     # # then we check if the requirement is one of the passed_courses
    #     # # if it's NOT PASSED, we add the required_for.all() in a list

    #     # level_restriction = []
    #     # if self.get_remaining_courses().filter(level=100).exists():
    #     #     level_restriction.append(300)
    #     # if self.get_remaining_courses().filter(level=200).exists():
    #     #     level_restriction.append(400)
    #     # if self.get_remaining_courses().filter(level=300).exists():
    #     #     level_restriction.append(500)

    #     # prereqs_restriction = [course.code for course in list(dict.fromkeys(prerequisites_restriction))]
    #     # restriction = dict(
    #     # [('Prerequisites Restriction', self.get_remaining_courses().filter(
    #     #     code__in=prereqs_restriction)),
    #     #  ('Level Restriction', self.get_remaining_courses().filter(
    #     #      level__in=level_restriction))]
    #     # )

    #     # return restriction

    # def get_period_course_restriction(self):
    #     """"""
    #     pass

    # # def get_progress(self):
    # #     results = self.get_prettier_results()[0]
    # #     degree = self.get_degree()
    # #     courses = self.get_degree().courses.all()
    # #     degree_progress = dict([(str(degree), {})])
    # #     degree_progress[str(degree)].update({'Courses': []})
    # #     degree_progress[str(degree)].update({'Statistics': {}})

    # #     progress = degree_progress[str(degree)]

    # #     for course in courses:
    # #         if (
    # #             self.get_passed_courses().filter(
    # #                 code=course.code).exists() or
    # #                 self.get_passed_courses().filter(
    # #                     course__in=course.equalled_courses.all())):
    # #             progress['Courses'].append({
    # #                 'code': course.code, 'name_en': course.name_en,
    # #                 'credit': course.credit, 'status': 'Passed'})
    # #         elif self.get_failed_courses().filter(code=course.code).exists():
    # #             progress['Courses'].append({
    # #                 'code': course.code, 'name_en': course.name_en,
    # #                 'credit': course.credit, 'status': 'Failed'})
    # #         elif self.get_enroled_courses().filter(
    # #         code=course.code, grade=None).exists():
    # #             progress['Courses'].append({
    # #                 'code': course.code, 'name_en': course.name_en,
    # #                 'credit': course.credit,
    # #                 'status': 'No grade'})
    # #         elif (self.get_enrolment_restriction(
    # #         )['Prerequisites Restriction'].filter(
    # #         code=course.code).exists() or self.get_enrolment_restriction(
    # #         )['Level Restriction'].filter(
    # #         code=course.code).exists()):
    # #             progress['Courses'].append({
    # #                 'code': course.code, 'name_en': course.name_en,
    # #                 'credit': course.credit,
    # #                 'status': 'Restricted'})
    # #         else:
    # #             progress['Courses'].append({
    # #                 'code': course.code, 'name_en': course.name_en,
    # #                 'credit': course.credit,
    # #                 'status': 'Possible to Enroll'})

    # #     # for i in results['Periods']:
    # #     cumulative_GPAs = [results['Results'][i]['Statistics']['cumulative_GPA'] for i in results['Periods']]
    # #     period_GPAs = [results['Results'][i]['Statistics']['GPA'] for i in results['Periods']]
    # #     periods = results['Periods']
    # #     last_period = results['Periods'][-1]

    # #     actual_period_count = results['Results'][last_period]['Statistics']['actual_period_count']
    # #     completed_credits = courses.filter(
    # #         code__in=self.get_passed_courses().values_list(
    # #             'code', flat=True)).aggregate(Sum('credit')).values()[0]
    # #     required_credits = courses.aggregate(Sum('credit')).values()[0]
    # #     average_performance = completed_credits/float(actual_period_count)
    # #     estimated_number_of_periods = int(required_credits/average_performance)
    # #     completion_percentage = int(100*completed_credits/required_credits)

    # #     progress['Statistics'].update(
    # #         {'GPA': period_GPAs,
    # #          'cumulative_GPA': cumulative_GPAs,
    # #          'actual_period_count': actual_period_count,
    # #          'completed_credits': completed_credits,
    # #          'required_credits': required_credits,
    # #          'average_performance': average_performance,
    # #          'estimated_number_of_periods': estimated_number_of_periods,
    # #          'periods': periods,
    # #          'completion_percentage': completion_percentage
    # #      })

    # #     return [degree_progress]

    #     #return not_possible_to_enrol

    # # def get_absolute_url(self):
    # #     return reverse('student-home',
    # #                    kwargs={
    # #                        'registration_number': self.registration_number,
    # #                    }
    # #     )
