# # from .models import StudentResult
# # from .section_enrolments.models import SectionEnrolment


# def get_results(student):



    # def get_allowed_enrolments(self):




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
