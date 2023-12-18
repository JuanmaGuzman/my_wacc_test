from django import forms

class DateSelectionForm(forms.Form):
    selected_date = forms.DateField(label='¿Want to know Bitcoin value on a specific day?', widget=forms.DateInput(attrs={'type': 'date'}))

class DateRangeSelectionForm(forms.Form):
    start_date = forms.DateField(label='Bitcoin average from:', widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(label='To:', widget=forms.DateInput(attrs={'type': 'date'}))