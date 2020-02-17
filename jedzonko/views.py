from datetime import datetime


from django.shortcuts import render, HttpResponse, redirect
from random import shuffle
import time
from django.shortcuts import render
from django.views import View
from jedzonko.models import *
from django.core.paginator import Paginator


class IndexView(View):

    def get(self, request):
        ctx = {"actual_date": datetime.now()}
        return render(request, "test.html", ctx)


class NewIndexView(View):

    def get(self, request):
        coupon_items = list(Recipe.objects.all())
        shuffle(coupon_items)
        one = coupon_items[0]
        two = coupon_items[1]
        three = coupon_items[2]
        return render(request, "index.html", {'one': one, 'two': two, 'three': three})


class DashboardView(View):

    def get(self, request):
        recipes_count = Recipe.objects.count()
        recipes_count = str(recipes_count)
        plans_count = Plan.objects.count()
        plans_count = str(plans_count)
        return render(request, "dashboard.html", {'recipes_count': recipes_count, 'plans_count': plans_count})


class RecipeList(View):

    def get(self, request):
        recipes_list = Recipe.objects.all().order_by('-votes', '-created')
        paginator = Paginator(recipes_list, 50)
        page = request.GET.get('page')
        recipes = paginator.get_page(page)
        return render(request, "app-recipes.html", {"recipes": recipes})

class AddRecipe(View):
    def get(self, request):
        wrong_data = False
        if request.session.get('wrong_data') is not None:
            wrong_data = request.session.get('wrong_data')
            del request.session['wrong_data']
        return render(request, 'app-add-recipe.html', {'wrong_data': wrong_data})

    def post(self, request):
        name = request.POST.get('name')
        ingredients = request.POST.get('ingredients')
        description = request.POST.get('description')
        preparation_time = 0
        if request.POST.get('preparation_time') != '':
            preparation_time = int(request.POST.get('preparation_time'))
        if name != ''\
            and ingredients != ''\
            and description != ''\
            and preparation_time != 0:
            Recipe.objects.create(name=name,
                                 ingredients=ingredients,
                                 description=description,
                                 preparation_time=preparation_time)
            return redirect('/recipe/list/')
        else:
            request.session['wrong_data'] = True
            return redirect('/recipe/add/')


class RecipeDetails(View):
    def get(self, request):
        return render(request, 'blank.html')


class RecipeEdit(View):
    def get(self, request):
        return render(request, 'blank.html')


class PlanDetails(View):
    def get(self, request):
        return render(request, 'blank.html')


class PlanAdd(View):
    def get(self, request):
        return render(request, 'app-add-schedules.html')

    def post(self, request):
        name = request.POST.get('planName')
        description = request.POST.get('planDescription')
        if name and description:
            Plan.objects.create(name=name, description=description)
            return redirect('/plan/list/')
        else:
            return HttpResponse("Uzupełnij dane")


class PlanAddRecipe(View):
    def get(self, request):
        return render(request, 'blank.html')


class PlanList(View):
    def get(self, request):
        return render(request, 'blank.html')

