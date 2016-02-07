# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.mail import send_mail

# from ....notifications import Notification


def send_assessment_result_email(assessment_result):

    if assessment_result.assessment.result_status == 'P':
        course = assessment_result.assessment.period_course.course
        total_grade = assessment_result.assessment.total_grade
        grade = assessment_result.grade
        message = (
            "Dear Student \n A new result has been submitted in "
            "your records: \n {}: {}/{} \n If you have any issues "
            "please do not reply to this email and contact Learning "
            "and Examination office.".format(course, total_grade, grade))

        send_mail('Results',
                  message,
                  'lande@aerodept.edu.ly',
                  ['student@aerodept.edu.ly'],
                  fail_silently=False)
