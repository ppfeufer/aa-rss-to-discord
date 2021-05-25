"""
Managers for our models
"""

from django.db import models


class RssFeedsManager(models.Manager):
    """
    AFatManager
    """

    def select_enabled(self):
        """
        Apply select_related for default query optimizations.
        """

        return self.filter(enabled=True)
