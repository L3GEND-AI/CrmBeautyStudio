from django import forms
from .models import Services

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Services
        fields = ['name_service', 'price', 'category_service', 'description', 'slug']
        widgets = {
            'name_service': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'category_service': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
        }

