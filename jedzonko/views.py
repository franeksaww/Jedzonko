from datetime import datetime
from random import shuffle
import time
from django.shortcuts import render
from django.views import View

from jedzonko.models import Recipe


class IndexView(View):

    def get(self, request):
        ctx = {"actual_date": datetime.now()}
        return render(request, "test.html", ctx)


class NewIndexView(View):

    def get(self, request):
        coupon_items = list(Recipe.objects.all())
        shuffle(coupon_items)
        recipe_1 = coupon_items[0]
        recipe_2 = coupon_items[1]
        recipe_3 = coupon_items[2]
        return render(request, "index.html", {'recipe_1': recipe_1, 'recipe_2': recipe_2, 'recipe_3': recipe_3})


class RecipeList(View):

    def get(self, request):
        return render(request, "app-recipes.html")


