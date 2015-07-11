from django.utils.translation import ugettext_lazy as _
# from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError


def validate_grade(grade):
    """"""
    if not(grade):
        pass
    else:
        if grade > 100 or grade < 0:
            raise ValidationError(
                _('Grade cannot be greater than 100 or less than 0')
             )


# I may not need the above code at all
# think of this:
#         return MaxValueValidator(100,
#                                  message=_('Grade cannot be greater than 100')),
# MinValueValidator(0,
#                   message=_('Grade cannot be less than 0'))
