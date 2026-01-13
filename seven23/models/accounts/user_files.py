from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from seven23.models.accounts.models import Account

# print("LOADING user_files.py")

class UserFile(models.Model):
    account = models.ForeignKey(
        Account,
        related_name="files",
        on_delete=models.CASCADE
    )
    uploaded_by = models.ForeignKey(
        User,
        related_name="uploaded_files",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    title = models.CharField(_("Title"), max_length=255, blank=True)
    file = models.FileField(upload_to="user_uploads/%Y/%m/%d/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-uploaded_at",)

    def __str__(self):
        return f"{self.account_id} - {self.title or self.file.name}"
