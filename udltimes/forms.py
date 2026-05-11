import re
from django import forms
from .models import CustomWordle

class WordleForm(forms.ModelForm):
    class Meta:
        model = CustomWordle
        fields = ['word']
        widgets = {
            'word': forms.TextInput(attrs={
                'class': 'w-full mt-1 px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-[#700040] focus:border-transparent uppercase',
                'placeholder': 'Ej: CORES',
                'maxlength': '5'
            })
        }

    def clean_word(self):
        word = self.cleaned_data.get('word', '').strip().upper()

        if len(word) != 5:
            raise forms.ValidationError("The word must be exactly 5 letters long.")

        if not re.match(r'^[A-ZÁÉÍÓÚÜÑ]+$', word):
            raise forms.ValidationError("Only letters are allowed.")

        return word