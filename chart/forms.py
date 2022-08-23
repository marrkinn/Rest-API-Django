from pyexpat import model
from django import forms
from django.forms import ModelForm
from chart.models import FormDateRange

class FormDate(ModelForm):
    class Meta:
        model = FormDateRange
        widgets = {
            'start_date': forms.DateInput(attrs={'placeholder': 'YYYY-MM-DD','class':'form-control'}),
            'end_date': forms.DateInput(attrs={'placeholder': 'YYYY-MM-DD','class':'form-control'}),         
        }
        fields = "__all__"