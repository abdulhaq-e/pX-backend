from django.db import models


# class ValidateOnSaveMixin(object):

#     def save(self, force_insert=False, force_update=False, **kwargs):
# #        if not (force_insert or force_update):
#         self.full_clean()
#         super(ValidateOnSaveMixin, self).save(force_insert, force_update,
#                                               **kwargs)

class pXBaseModel(models.Model):
    """
    """
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    notes = models.TextField(blank=True)

    class Meta:
        abstract = True
        ordering = ("modified_at", "created_at")
