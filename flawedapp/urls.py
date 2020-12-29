from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add/', views.add, name='add'),
    path('delete/', views.delete, name='delete'),
    path('details/<int:id>/', views.details, name='details'),
    path('list/', views.list, name='list'),
    path('card/', views.card, name='card'),
    path('account/', views.account, name='account'),
    path('search/', views.search, name='search'),
]