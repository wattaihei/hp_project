from django import forms

class SortForm(forms.Form):
    text = forms.CharField(label='input_word', widget=forms.TextInput)
