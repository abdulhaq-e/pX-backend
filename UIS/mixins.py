from django.views.generic.base import ContextMixin
from django.shortcuts import get_object_or_404
from UIS.models.time_period import Period
from UIS.models.students import Student


class StudentMixin(ContextMixin):
    """"""
    def get_context_data(self, **kwargs):
        context = super(StudentMixin, self).get_context_data(**kwargs)
        context['student'] = get_object_or_404(
            Student,
            registration_number=self.kwargs['registration_number']
        )

        return context

    #mixin = StudentMixin.get_context_data()


class PeriodMixin(ContextMixin):
    """"""
    def get_context_data(self, **kwargs):
        context = super(PeriodMixin, self).get_context_data(**kwargs)
        context['period'] = Period.objects.get_from_url(
            period=self.kwargs['period'],
            academic_year=self.kwargs['academic_year']
        )

        return context

    #mixin = get_context_data()
