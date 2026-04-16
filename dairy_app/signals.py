from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Payment, MonthlyBill
from datetime import date


@receiver(post_save, sender=Payment)
def update_bill_after_payment(sender, instance, **kwargs):
    customer = instance.customer

    # assume current month payment
    month = date.today().replace(day=1)

    bill, created = MonthlyBill.objects.get_or_create(
        customer=customer,
        month=month
    )

    # add payment
    bill.amount_paid += instance.amount_paid
    bill.balance = bill.total_amount - bill.amount_paid

    # update status
    if bill.balance <= 0:
        bill.status = "paid"
    elif bill.amount_paid == 0:
        bill.status = "pending"
    else:
        bill.status = "partial"

    bill.save()
