from django.db import models
from django.db.models import Sum, Count, Aggregate, F


class StudentEnrolmentQuerySet(models.QuerySet):
    """"""

    def enroled(self):
        return self.all()

    def passed(self, pass_grade=50):
        return self.filter(grade__gte=pass_grade)

    def failed(self, pass_grade=50):
        return self.filter(grade__lt=pass_grade)
    # def attempted_but_failed_courses(self, pass_grade=50):
    #     return self.filter(grade__lt=pass_grade)

    def get_statistics(self, credits=None, points=None):
        a = self.aggregate(
            credits=Sum(F('credit')),
            points=Sum(F('credit')*F('grade'),
                      output_field=models.FloatField())
        )
        for key, value in a.iteritems():
            if value is None:
                a[key] = 0
        #a['points'] = 1
        if credits:
            a[credits] = a.pop('credits')
        if points:
            a[points] = a.pop('points')

        return a


    # def get_term_statistics(self):
    #     return self.enroled_courses().aggregate(
    #         registered_credits=Sum('section__course__course__credit'),
    #         passed_credits=)
