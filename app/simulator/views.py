from django.shortcuts import render, redirect
from .forms import CardForm
from .models import EnglishCard

# Create your views here.

def index(request):
    return render(request, "index.html")

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