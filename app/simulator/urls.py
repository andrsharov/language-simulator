"""
urls.py
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('add_card/', views.add_card, name='add_card'),
    path('cards_list/', views.cards_list, name='cards_list'),
    path('exercise_card/', views.exercise_card, name='exercise_card'),
    path('no_cards/', views.no_cards, name='no_cards'),
    path('stats/', views.stats, name='stats'),
]
