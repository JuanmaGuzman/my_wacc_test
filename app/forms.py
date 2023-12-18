from django import forms

class DateSelectionForm(forms.Form):
    selected_date = forms.DateField(label='Select a date', widget=forms.DateInput(attrs={'type': 'date'}))
