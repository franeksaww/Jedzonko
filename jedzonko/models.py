from django.db import models


class Recipe(models.Model):
    name = models.CharField(max_length=128)
    ingredients = models.TextField()
    description = models.TextField()
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now_add=True)
    preparation_time = models.IntegerField(null=True)
    votes = models.IntegerField(default=0)

