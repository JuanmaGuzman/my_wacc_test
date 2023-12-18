# models.py
from django.db import models

class BitcoinPrice(models.Model):
    date = models.DateTimeField()
    value = models.FloatField()

    def __str__(self):
        return f"{self.date} - {self.value}"




# Apply the model changes to the database
# python manage.py makemigrations
# python manage.py migrate
