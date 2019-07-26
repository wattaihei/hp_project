from django import forms
from django.core.validators import MaxValueValidator, MinValueValidator

# from https://stackoverflow.com/questions/17159567/how-to-create-a-list-of-fields-in-django-forms
class SudokuForm(forms.Form):
    num = forms.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)], widget=forms.TextInput)