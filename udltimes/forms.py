from django import forms
from .models import Wordle

class WordleForm(forms.ModelForm):
    class Meta:
        model = Wordle
        fields = ['date', 'word'] # El autor se asigna automáticamente en la vista