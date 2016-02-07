# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.core import mail

import pytest

pytestmark = pytest.mark.django_db


class TestModels():
    def test_assessment_type_uniqueness(self, assessment_type_factory):

        with pytest.raises(IntegrityError):
            assessment_type_factory(assessment_type='Final Examination')
            assessment_type_factory(assessment_type='Course Work')

    def test_assessment_result_grade_validator(self,
                                               assessment_result_factory):

        with pytest.raises(ValidationError):
            assessment_result_factory(_grade=120)

        with pytest.raises(ValidationError):
            assessment_result_factory(_grade=-100)

        with pytest.raises(ValidationError):
            assessment_result_factory(_grade=21)

    def test_assessment_result_publishing(self, assessment_result_factory):

        assessment_result = assessment_result_factory()

        assert assessment_result.grade is None
        assert assessment_result._grade is None

        assessment_result2 = assessment_result_factory(
            assessment__result_status='P',
            _grade=10)

        assert assessment_result2.grade == 10

        assessment_result3 = assessment_result_factory(_grade=15, hidden=True)

        assert assessment_result3.grade is None
        assert assessment_result3._grade == 15

    def test_assessment_result_email(self, assessment_result_factory):

        assessment_result = assessment_result_factory(
            assessment__total_grade=100,
            assessment__result_status='P',
            _grade=100)

        assessment_result.send_email()

        assert len(mail.outbox) == 1
        assert mail.outbox[0].subject == "Results"
