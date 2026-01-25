from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from seven23.models.accounts.serializers import UserNotificationsSerializer
from seven23.models.accounts.user_notification import UserNotifications
from seven23.api.accounts.utils import resolve_account_for_user

class UserNotificationsView(generics.RetrieveAPIView,
    generics.CreateAPIView,
    generics.UpdateAPIView,):
        serializer_class = UserNotificationsSerializer
        permission_classes = [IsAuthenticated]

        def get_object(self):
            account = resolve_account_for_user(self.request.user)

            notifications, _created = UserNotifications.objects.get_or_create(
                account=account,
                defaults={
                    "notification_status": False,
                    "last_action": None,
                    "current_date_reminder": None,
                }
            )
            return notifications

        def perform_create(self, serializer):
             account = resolve_account_for_user(self.request.user)
             serializer.save(account=account)

        def perform_update(self, serializer):
            account = resolve_account_for_user(self.request.user)
            serializer.save(account=account)

