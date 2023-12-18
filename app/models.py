# models.py
from django.db import models

class BitcoinValue(models.Model):
    date = models.DateTimeField()
    value = models.FloatField()

    def __str__(self):
        return f"{self.date} - {self.value}"