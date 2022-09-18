from djangae.contrib.googleauth.models import AbstractGoogleUser
from django.conf import settings
from django.db import models
from django.utils import timezone


class TimeStampModel(models.Model):
    """Abstract base class for timestamp"""

    created_at = models.DateTimeField(blank=True, editable=False)
    modified_at = models.DateTimeField(blank=True, editable=False)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="%(class)s_created_by",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
    )
    modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="%(class)s_modified_by",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
    )

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = timezone.now()

        self.modified_at = timezone.now()

        return super().save(*args, **kwargs)


class User(AbstractGoogleUser):
    pass
