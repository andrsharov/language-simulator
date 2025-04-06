from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count, Case, When, IntegerField
from django.urls import reverse
from django.contrib import messages
from .forms import CardForm
from .models import EnglishCard, CardStatistics
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


def exercise_card(request):
    all_cards = list(EnglishCard.objects.all())

    if not all_cards:
        return render(request, 'no_cards.html')

    session_cards = request.session.get('exercise_cards', [])
    user_answer = request.POST.get('user_answer', '').strip().lower()
    is_correct = False

    if not session_cards:
        session_cards = [card.id for card in all_cards]
        random.shuffle(session_cards)
        request.session['exercise_cards'] = session_cards

    current_card_id = session_cards[0]
    current_card = get_object_or_404(EnglishCard, id=current_card_id)

    if request.method == 'POST' and 'check_answer' in request.POST:
        if not user_answer:
            messages.error(request, "Пожалуйста, введите ответ")
        else:
            is_correct = (user_answer == current_card.english_word.lower())
            # Сохраняем статистику
            CardStatistics.objects.create(
                card=current_card,
                is_successful=is_correct
            )
            # Добавляем сообщение о результате
            if is_correct:
                messages.success(request, "Правильно! 👍")
            else:
                messages.error(request, f"Неверно. Правильный ответ: {current_card.english_word}")

            # Удаляем карточку из сессии и переходим к следующей
            session_cards.pop(0)
            request.session['exercise_cards'] = session_cards
            return redirect(reverse('exercise_card'))

    return render(request, 'exercise_card.html', {
        'card': current_card,
        'user_answer': user_answer,
    })


def stats(request):
    # Получаем статистику по всем карточкам
    cards_stats = EnglishCard.objects.annotate(
        total_attempts=Count('statistics'),
        successful_attempts=Count(
            Case(
                When(statistics__is_successful=True, then=1),
                output_field=IntegerField()
            )
        ),
        failed_attempts=Count(
            Case(
                When(statistics__is_successful=False, then=1),
                output_field=IntegerField()
            )
        )
    ).order_by('id')

    # Рассчитываем процент успешных попыток для каждой карточки
    total_success_rate = 0
    cards_with_attempts = 0

    for card in cards_stats:
        if card.total_attempts > 0:
            card.success_rate = round((card.successful_attempts / card.total_attempts) * 100)
            total_success_rate += card.success_rate
            cards_with_attempts += 1
        else:
            card.success_rate = 0

    # Рассчитываем средний процент успеха
    average_success_rate = round(total_success_rate / cards_with_attempts) if cards_with_attempts > 0 else 0

    return render(request, 'stats.html', {
        'cards_stats': cards_stats,
        'total_cards': EnglishCard.objects.count(),
        'total_attempts': CardStatistics.objects.count(),
        'average_success_rate': average_success_rate,
    })