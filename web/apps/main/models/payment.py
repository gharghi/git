from django.db import models
from web.apps.jwt_store.models import User

class Payment(models.Model):
    amount = models.BigIntegerField(null=False, default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rfid = models.CharField(max_length=255, null=True, blank=True)
    authority = models.CharField(max_length=40, null=True, blank=True)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.amount)
