from django.db import models
from django.contrib.auth.models import User


class Doctor(models.Model):
    first_name = models.CharField(max_length=128)
    father_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    phone = models.BigIntegerField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    aca_degree = models.CharField(max_length=128, blank=True, null=True)
    contract_type = models.CharField(max_length=128, blank=True, null=True)
    is_archived = models.BooleanField(default=False)

    def archive(self):
        if not self.is_archived:
            self.is_archived = True
            self.save()

    def unarchive(self):
        if self.is_archived:
            self.is_archived = False
            self.save()

    def __str__(self):
        return f'{self.first_name} {self.father_name} {self.last_name}'
