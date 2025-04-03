from django import forms
from .models import EnglishCard

class CardForm(forms.ModelForm):
    class Meta:
        model = EnglishCard
        fields = ['russian_word', 'english_word', 'image']
        widgets = {
            'russian_word': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите слово на русском'
            }),
            'english_word': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter English word'
            }),
        }

    def clean_russian_word(self):
        word = self.cleaned_data['russian_word']
        if not word.isalpha():
            raise forms.ValidationError("Используйте только буквы русского алфавита")
        return word.capitalize()

    def clean_english_word(self):
        word = self.cleaned_data['english_word']
        if not all(c.isalpha() or c.isspace() for c in word):
            raise forms.ValidationError("Use only English letters")
        return word.lower()