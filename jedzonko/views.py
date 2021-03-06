from datetime import datetime


from django.shortcuts import render, HttpResponse, redirect
from random import shuffle
import time
from django.shortcuts import render, get_object_or_404
from django.views import View
from jedzonko.models import *
from django.core.paginator import Paginator


class IndexView(View):

    def get(self, request):
        ctx = {"actual_date": datetime.now()}
        return render(request, "test.html", ctx)


class NewIndexView(View):

    def get(self, request):
        recipe_items = list(Recipe.objects.all())
        shuffle(recipe_items)
        one = recipe_items[0]
        two = recipe_items[1]
        three = recipe_items[2]
        plans = Plan.objects.all().order_by('-created')
        newest_plan = plans[0]
        try:
            link_about = Page.objects.get(title='about')
        except Exception:
            link_about = None
        try:
            link_contact = Page.objects.get(title='contact')
        except Exception:
            link_contact = None
        return render(request, "index.html", {'one': one, 'two': two, 'three': three, 'newest_plan': newest_plan, 'link_about': link_about, 'link_contact': link_contact})


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
    def get(self, request, id):
        recipe = get_object_or_404(Recipe, pk= id)
        return render(request, 'app-recipe-details.html', {"recipe": recipe })

    def post(self, request, id):
        recipe = get_object_or_404(Recipe, pk=id)
        if 'upvote' in request.POST:
            recipe.votes += 1
            recipe.save()
        elif 'downvote' in request.POST:
            recipe.votes -= 1
            recipe.save()
        return redirect(f'/recipe/{id}')


class RecipeEdit(View):
    def get(self, request, id):
        wrong_data = False
        if request.session.get('wrong_data') is not None:
            wrong_data = request.session.get('wrong_data')
            del request.session['wrong_data']
        recipe = get_object_or_404(Recipe, pk=id)
        return render(request, 'app-edit-recipe.html', {"recipe": recipe, 'wrong_data': wrong_data})

    def post(self, request, id):
        name = request.POST.get('name')
        ingredients = request.POST.get('ingredients')
        description = request.POST.get('description')
        preparation_time = 0
        if request.POST.get('preparation_time') != '':
            preparation_time = int(request.POST.get('preparation_time'))
        if name != '' \
                and ingredients != '' \
                and description != '' \
                and preparation_time != 0:
            Recipe.objects.create(name=name,
                                  ingredients=ingredients,
                                  description=description,
                                  preparation_time=preparation_time)
            return redirect('/recipe/list/')
        else:
            request.session['wrong_data'] = True
            return redirect(f'/recipe/modify/{id}/')


class PlanDetails(View):
    def get(self, request, id):
        recipe_tab = [[] for _ in range(7)]
        order_tab = [[] for _ in range(7)]
        meals_tab = [[] for _ in range(7)]
        meal_names = RecipePlan.MEALS
        day_names = Dayname.DAYS_OF_WEEK
        plan = get_object_or_404(Plan, pk=id)
        plan_details = RecipePlan.objects.filter(plan=id)
        for detail in plan_details:
            recipe_id = detail.recipe_id
            day_name_id = detail.day_name.name
            recipe = Recipe.objects.get(pk=recipe_id)
            if not recipe_tab[day_name_id]:
                recipe_tab[day_name_id].append(recipe)
                order_tab[day_name_id].append(detail.day_name.order)
                meals_tab[day_name_id].append(detail.meal_name)
            else:
                index = 0
                for i in range(len(recipe_tab[day_name_id])):
                    if order_tab[day_name_id][i] < detail.day_name.order:
                        index += 1
                recipe_tab[day_name_id].insert(index, recipe)
                order_tab[day_name_id].insert(index, detail.day_name.order)
                meals_tab[day_name_id].insert(index, detail.meal_name)
        return render(request,
                      'app-details-schedules.html',
                      {"plan": plan, "meals_tab": meals_tab, "recipe_tab": recipe_tab,"meal_names":meal_names, "day_names":day_names}
                      )

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
        recipes = Recipe.objects.all()
        plans = Plan.objects.all()
        days = Dayname.DAYS_OF_WEEK
        meal_names = RecipePlan.MEALS
        number_exsist = False
        if request.session.get('number_exsist') is not None:
            number_exsist = request.session.get('number_exsist')
            del request.session['number_exsist']
        return render(request,
                      'app-schedules-meal-recipe.html',
                      {"recipes": recipes,
                       "plans": plans,
                       "days": days,
                       "meal_names": meal_names,
                       "number_exsist": number_exsist})

    def post(self, request):
        meal_id = int(request.POST.get('meal_id'))
        plan_id = request.POST.get('plan_id')
        recipe_id = request.POST.get('recipe_id')
        day = int(request.POST.get('day'))
        number = int(request.POST.get('meal_number'))
        try:
            day_obj = Dayname.objects.get(name=day, order=number)
        except Dayname.DoesNotExist:
            day_obj = Dayname.objects.create(name=day, order=number)
        try:
            recipe_plan_obj = RecipePlan.objects.get(plan_id=plan_id, day_name_id=day_obj.id)
            request.session['number_exsist'] = True
            return redirect('/plan/add-recipe/')

        except RecipePlan.DoesNotExist:
            RecipePlan.objects.create(meal_name=meal_id,
                                      plan_id=plan_id,
                                      recipe_id=recipe_id,
                                      day_name_id=day_obj.id)
            return redirect(f'/plan/{plan_id}/')


class PlanList(View):
    def get(self, request):
        plans_list = Plan.objects.all().order_by('name')
        paginator = Paginator(plans_list, 50)
        page = request.GET.get('page')
        plans = paginator.get_page(page)
        return render(request, "app-schedules.html", {"plans": plans})


class About(View):

    def get(self, request):
        try:
            link_about = Page.objects.get(title='about')
        except Exception:
            link_about = None
        try:
            link_contact = Page.objects.get(title='contact')
        except Exception:
            link_contact = None
        return render(request, 'about.html', {'link_contact': link_contact, 'link_about': link_about})


class Contact(View):

    def get(self, request):
        try:
            link_about = Page.objects.get(title='about')
        except Exception:
            link_about = None
        try:
            link_contact = Page.objects.get(title='contact')
        except Exception:
            link_contact = None
        return render(request, 'contact.html', {'link_contact': link_contact, 'link_about': link_about})


"""Z na stronie listy przepisów, należy dodać działający link do strony głównej aplikacji: /main/"""