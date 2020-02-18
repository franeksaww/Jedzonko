
from django.contrib import admin
from django.urls import path, re_path
from jedzonko.views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', IndexView.as_view()),
    path('', NewIndexView.as_view()),
    re_path('recipe/(?P<id>[0-9]*)/$', RecipeDetails.as_view()),
    path('recipe/list/', RecipeList.as_view()),
    path('recipe/modify/<int:id>/', RecipeEdit.as_view()),
    path('recipe/add/', AddRecipe.as_view()),
    path('main/', DashboardView.as_view()),
    re_path('plan/(?P<id>[0-9]*)/$', PlanDetails.as_view()),
    path('plan/add/', PlanAdd.as_view()),
    path('plan/add-recipe/', PlanAddRecipe.as_view()),
    path('plan/list/', PlanList.as_view())
]
