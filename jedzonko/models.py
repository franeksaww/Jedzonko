from django.db import models
from django.utils import timezone


class Recipe(models.Model):
    name = models.CharField(max_length=255)
    ingredients = models.TextField()
    description = models.TextField()
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now_add=True)
    preparation_time = models.IntegerField(null=True)
    votes = models.IntegerField(default=0)


class Plan(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    created = models.DateTimeField(default=timezone.now)
    recipes = models.ManyToManyField(Recipe,through="RecipePlan")

    
class Dayname(models.Model):
    DAYS_OF_WEEK = (
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
        (6, 'Sunday'),
    )
    name = models.CharField(max_length=16,choices=DAYS_OF_WEEK)
    order = models.IntegerField(unique=True)

    
class RecipePlan(models.Model):
    MEALS = (
        (0,'Śniadanie'),
        (1,'Drugie śniadanie'),
        (2,'Obiad'),
        (3,'Podwieczorek'),
        (4,'Kolacja'),
    )
    meal_name = models.CharField(max_length=255, choices=MEALS)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    order = models.IntegerField()
    day_name = models.ForeignKey(Dayname, on_delete=models.CASCADE)



