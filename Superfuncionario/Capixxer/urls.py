from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('comparativo/', views.comparativo, name='comparativo'),
    path('inserir-dados/', views.inserir_dados, name='inserir_dados'),
]
