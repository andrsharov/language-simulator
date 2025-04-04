from django.db import models
from django.core.validators import MinLengthValidator

# Create your models here.

class EnglishCard(models.Model):
    russian_word = models.CharField(
        max_length=100,
        verbose_name="Слово на русском",
        validators=[MinLengthValidator(2, "Слово должно содержать минимум 2 буквы")]
    )
    english_word = models.CharField(
        max_length=100,
        verbose_name="Слово на английском",
        validators=[MinLengthValidator(2, "Слово должно содержать минимум 2 буквы")]
    )
    image = models.ImageField(
        upload_to='cards_images/',
        verbose_name="Картинка",
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Карточка английского"
        verbose_name_plural = "Карточки английского"

    def __str__(self):
        return f"{self.russian_word} - {self.english_word}"