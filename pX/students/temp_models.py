# -*- coding: utf-8 -*-
from __future__ import division, unicode_literals

from django.db import models

import uuid


class StudentResult(models.Model):
    '''
    THIS SHOULD BE A MATERIALIZED VIEW, I DON'T LIKE THE CURRENT IMPLEMENTATION.
    '''

    student_results_id = models.UUIDField(primary_key=True,
                                          default=uuid.uuid4,
                                          editable=False)

    period_registration = models.OneToOneField(
        'period_registrations.PeriodRegistration',
        related_name='student_result')

    period_count = models.IntegerField()
    actual_period_count = models.IntegerField()

    registered_credits = models.FloatField()
    passed_credits = models.FloatField()
    repeated_credits = models.FloatField()
    cumulative_registered_credits = models.FloatField()
    cumulative_passed_credits = models.FloatField()

    scored_points = models.FloatField()
    passed_points = models.FloatField()
    repeated_points = models.FloatField()
    cumulative_scored_points = models.FloatField()

    GPA = models.FloatField()
    cumulative_GPA = models.FloatField()
    previous_GPA = models.FloatField()

    warnings = models.IntegerField()
    previous_warnings = models.IntegerField()
    very_poor_warnings = models.IntegerField(default=0)
    expulsion = models.IntegerField(default=False)

    class Meta:
        ordering = (
            'period_registration',
        )
