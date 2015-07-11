from django.db import models
from django.utils.translation import ugettext_lazy as _
from linguo.models import MultilingualModel
from UIS.managers import MultilingualNameManager, MultilingualDeptManager
from UIS.models.base_model import UISBaseModel


class Administration(MultilingualModel, UISBaseModel):

    name = models.CharField(max_length=60, unique=True,
                               verbose_name=_('Name of Faculty'))
    # we can't have two administrations(?) using the same name.
    # head = models.ForeignKey('Employee', blank=True, null=True,
    #                          related_name='head_of_%(class)s',
    #                          on_delete=models.PROTECT)
    # pa_to_head = models.ForeignKey('Employee', blank=True, null=True,
    #                                related_name='pa_to_head_of_%(class)s',
    #                                on_delete=models.PROTECT)
    # WHY IS THE ABOVE COMMENTED OUT: BECAUSE I STILL NEED TO REVIEW PERMISSIONS
    # IT'S VERY LIKELY THAT I WILL NOT NEED THE ABOVE FIELDS!

    objects = MultilingualNameManager()

    def __unicode__(self):
        return self.name

    class Meta:
        app_label = 'UIS'
        abstract = True
        translate = ('name',)


class Faculty(Administration):
    """The Faculty tables should list the faculties in the universities along with
    related attributes.

    random thoughts:

    - the head and personal assistant to head are obviously needed
      later for permission purposes, perhaps other fields are required to
      represent other adminstrative tasks such as projects coordinator or
      learningANDexamination coordinator BUT WAIT: perhaps django has other
      ways of handling permissions?
    - test, TODO: Search for django permission handling or in general how to handle permissions in web
      apps (canvas for example)

    """

    class Meta:
        app_label = 'UIS'
        verbose_name = 'Faculty'
        verbose_name_plural = 'Faculties'

    def natural_key(self):
        return (self.name,)


class Department(Administration):
    """
    exact copy of faculty, same notes

    random thoughts:

    - wait a moment, if this is an exact copy of faculty, why not subclass it?????
    - mmm: TODO: think of subclassing
    """

    acronym = models.CharField(max_length=3)
    faculty = models.ForeignKey('Faculty', on_delete=models.PROTECT)
    domain_name = models.CharField(max_length=255, blank=True)

    objects = MultilingualDeptManager()

    class Meta:
        app_label = 'UIS'

    def natural_key(self):
        return (self.name,) + self.faculty.natural_key()
    natural_key.dependencies = ['UIS.faculty']

    # class Facility(models.Model):
#     """
#     ALL UNIVERSITY FACILITIES SHOULD GO HERE, EVERYTHING (EVEN A WARDROBE).
#     """

#     FACILITY_TYPES = (
#         ('C', 'Class Room'),
#         ('H', 'Hall'),
#         ('O', 'Office'),
#     )

#     facility_name = models.CharField(max_length=20)
#     facility_alias = models.CharField(max_length=50, null=True)
#     facility_type = models.CharField(max_length=20, choices=FACILITY_TYPES)
#     facility_actual_capacity = models.SmallIntegerField(
#         verbose_name=_('facility capacity')
#     )
#     facility_theoritical_capacity = models.SmallIntegerField(
#         verbose_name=_('facility theoritical capacity'),
#         blank=True)
#     facility_location = models.CharField(max_length=20)
#     is_conditioned = models.BooleanField(
#         verbose_name=_('air conditioned?'),
#         default=False)
#     notes = models.TextField(blank=True)

#     def __unicode__(self):
#         return self.facility_name + ' (' + self.facility_alias + ')'


'''
class FacilityReservation(models.Model):

term = models.ForeignKey(Term, null=True, blank=True)
section = models.ForeignKey(Section, null=True, blank=True)
facility = models.ForeignKey(Facility)
slot = models.ForeignKey('TimeSlot')

class Meta:
unique_together = ('facility', 'slot', 'term',)

def __unicode__(self):
return self.facility.__unicode__() + ' ' + self.slot.__unicode__()
'''

# class TimeSlot(models.Model):
#     """
#     TODO: Everything to do with calenders needs to be reviewed

#     for example, the week order should be made flexible and not hard coded as
#     it is right now.
#     """
#     FRIDAY = 0
#     SATURDAY = 1
#     SUNDAY = 2
#     MONDAY = 3
#     TUESDAY = 4
#     WEDNESDAY = 5
#     THURSDAY = 6
#     DAYS = (
#         (FRIDAY, _('Friday')),
#         (SATURDAY, _('Saturday')),
#         (SUNDAY, _('Sunday')),
#         (MONDAY, _('Monday')),
#         (TUESDAY, _('Tuesday')),
#         (WEDNESDAY, _('Wednesday')),
#         (THURSDAY, _('Thursday')),
#     )

#     day = models.CharField(max_length=2, choices=DAYS)
#     starting_time = models.TimeField()
#     ending_time = models.TimeField()
#     time_format = '%H:%M'

#     class Meta:
#         unique_together = ('day', 'starting_time', 'ending_time',)
#         ordering = ['day', 'starting_time', 'ending_time']
#         # order_with_respect_to = 'day'

#     def __unicode__(self):
#         return self.get_day_display() + ' ' + self.starting_time.strftime(self.time_format) + \
#             ' - ' + self.ending_time.strftime(self.time_format)


# class TimeTable(models.Model):
#     """
#     again, this needs to be reviewed, put it in the target plan near the top!
#     """

#     slot = models.ForeignKey('TimeSlot')
#     section = models.ForeignKey('Section', blank=True,
#                                 on_delete=models.PROTECT)
#     # term = models.ForeignKey(Section, to_field='term')
#     facility = models.ForeignKey('Facility',
#                                  blank=True, on_delete=models.PROTECT)

#     class Meta:
#         unique_together = (('section', 'slot'), ('slot', 'facility',))
