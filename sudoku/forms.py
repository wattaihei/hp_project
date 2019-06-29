from django import forms
from django.core.validators import MaxValueValidator, MinValueValidator

class SudokuForm(forms.Form):
    num = forms.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)], widget=forms.TextInput)
