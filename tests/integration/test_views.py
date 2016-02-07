# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import IntegrityError
from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError
from django.core import mail

import pytest

pytestmark = pytest.mark.django_db


def test_period_course_view(client, assessment_result_factory,
                            period_course_factory, course_factory):

    url = reverse('period_courses-list')
    assessment_result = assessment_result_factory()
    period_course = period_course_factory()
    course = course_factory()
    # print(url)
    new_url = url + '/' + str(assessment_result.assessment.period_course.pk) \
              +'?include=course,assessments'#,assessments.assessment_results'
    response = client.get(new_url)
    # print(new_url)
    print(response.content)
    assert 0
