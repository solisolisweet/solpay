from django.db import models
from marketplace.models import Order

class CBETransaction(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='cbe_transaction')
    cbe_account_target = models.CharField(max_length=50, default="96072775", help_text="Bank of Abyssinia Target Account")
    cbe_ref_number = models.CharField(max_length=100, help_text="Bank of Abyssinia Mobile Banking or Transfer Reference Number")
    sender_name_or_phone = models.CharField(max_length=100)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    verified = models.BooleanField(default=False)
    verified_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"BOA Ref: {self.cbe_ref_number} -> Account 96072775 ({'VERIFIED' if self.verified else 'PENDING'})"

class PayoutLog(models.Model):
    cbe_account = models.CharField(max_length=50, default="96072775")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=30, default="SETTLED_INSTANT")
    transaction_note = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payout {self.amount} ETB to Bank of Abyssinia Account {self.cbe_account} [{self.status}]"

