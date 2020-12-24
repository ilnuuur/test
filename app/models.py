"""
Definition of models.
"""

from django.db import models

# Create your models here.
class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    long = models.FloatField()
    lat = models.FloatField()
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Restaurant'
        verbose_name_plural = 'Restaurants'
