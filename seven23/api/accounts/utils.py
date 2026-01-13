from rest_framework.exceptions import ValidationError
from django.db import transaction

from seven23.models.accounts.models import Account, AccountGuests
from seven23.models.currency.models import Currency


def _pick_default_currency():
    return (
        Currency.objects.filter(code__iexact="ILS").first()
        or Currency.objects.filter(code__iexact="USD").first()
        or Currency.objects.first()
    )


@transaction.atomic
def create_default_account_for_user(user):
    default_currency = _pick_default_currency()
    if not default_currency:
        raise ValidationError({"currency": "No currencies exist in DB to create default account."})

    acc = Account.objects.create(
        owner=user,
        name="Default",
        currency=default_currency,
        preferences="{}",
        archived=False,
        public=False,
    )
    acc.currencies.add(default_currency)  
    return acc


def resolve_account_for_user(user):
    # 1) owner
    acc = Account.objects.filter(owner=user, archived=False).order_by("create", "name").first()
    if acc:
        return acc

    guest_row = AccountGuests.objects.select_related("account").filter(
        user=user,
        account__archived=False
    ).order_by("account__create").first()
    if guest_row:
        return guest_row.account

    return create_default_account_for_user(user)
