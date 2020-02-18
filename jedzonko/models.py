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
    created = models.DateTimeField(auto_now_add=True, null=True)
    recipes = models.ManyToManyField(Recipe, through="RecipePlan")

    
class Dayname(models.Model):
    DAYS_OF_WEEK = (
        (0, 'Poniedziałek'),
        (1, 'Wtorek'),
        (2, 'Środa'),
        (3, 'Czwartek'),
        (4, 'Piątek'),
        (5, 'Sobota'),
        (6, 'Niedziela'),
    )
    name = models.IntegerField(choices=DAYS_OF_WEEK)
    order = models.IntegerField()

    
class RecipePlan(models.Model):
    MEALS = (
        (0, 'Śniadanie'),
        (1, 'Drugie śniadanie'),
        (2, 'Obiad'),
        (3, 'Podwieczorek'),
        (4, 'Kolacja'),
    )
    meal_name = models.IntegerField(choices=MEALS)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    day_name = models.ForeignKey(Dayname, on_delete=models.CASCADE)


class Page(models.Model):
    title = models.CharField(max_length=128, unique=True)
    description = models.TextField()
    slug = models.TextField(default=f'/{title}/')
