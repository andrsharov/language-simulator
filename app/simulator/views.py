from django.shortcuts import render, redirect
from .forms import CardForm
from .models import EnglishCard
import random

# Create your views here.

def index(request):
    all_cards = list(EnglishCard.objects.all())
    random_cards = random.sample(all_cards, min(3, len(all_cards))) if all_cards else []
    return render(request, "index.html",{'random_cards': random_cards})

def about(request):
    return render(request, "about.html")


def add_card(request):
    if request.method == 'POST':
        form = CardForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('cards_list')  # Перенаправляем после успешного сохранения
    else:
        form = CardForm()

    return render(request, 'add_card.html', {'form': form})

def cards_list(request):
    cards = EnglishCard.objects.all().order_by('-created_at')
    return render(request, 'cards_list.html', {'cards': cards})