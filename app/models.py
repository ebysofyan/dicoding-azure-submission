"""
app.models
"""
from django.db import models

# Create your models here.


class Programming(models.Model):
    """Programming Table"""
    name = models.CharField(max_length=100)
    year = models.CharField(max_length=100)
    creator = models.CharField(max_length=100)
    frameworks = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'programming'
        ordering = ['-year']
