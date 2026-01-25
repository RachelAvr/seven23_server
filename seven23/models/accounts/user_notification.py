from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


from seven23.models.accounts.models import Account

class UserNotifications(models.Model):
    account = models.OneToOneField(
        Account,
        related_name="notifications",
        on_delete=models.CASCADE
    )

    notification_status = models.BooleanField( default=False, blank=True)
    last_action = models.DateField(default=timezone.now)
    current_date_reminder=models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.account_id} - {self.last_action or self.current_date_reminder}"

