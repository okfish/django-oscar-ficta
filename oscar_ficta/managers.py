from django.db import models


class BrowsablePersonManager(models.Manager):
    """For searching/creating active juristic persons only."""
    status_filter = True

    def get_queryset(self):
        return super(BrowsablePersonManager, self).get_queryset().filter(
            is_active=self.status_filter)