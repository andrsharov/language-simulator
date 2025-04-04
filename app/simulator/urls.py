from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('add_card/', views.add_card, name='add_card'),
    path('cards_list/', views.cards_list, name='cards_list'),
]