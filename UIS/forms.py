from django import forms
from django.forms.models import modelformset_factory, ModelForm
from UIS.models.students import StudentRegistration


# class EnrolForm(forms.Form):
#     """"""
#     term_course = forms.ModelChoiceField(queryset=None)
#     group = forms.ModelChoiceField(queryset=None)

# EnrolFormSet = modelformset_factory(EnrolForm)
# class PeriodResultsForm(ModelForm):
#     class Meta:
#         model = StudentRegistration
#         fields = ('period',)
