from django import forms
from .models import Services, Blognews, User

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

class BlognewsForm(forms.ModelForm):
    class Meta:
        model = Blognews
        fields = ['tittle', 'description', 'image', 'maintext']
        widgets = {
            'tittle': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите заголовок'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Введите краткое описание'}),
            'image': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите URL изображения'}),
            'maintext': forms.Textarea(attrs={'class': 'form-control', 'rows': 10, 'placeholder': 'Введите основной текст'}),
        }

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'PhoneNumber']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'PhoneNumber': forms.TextInput(attrs={'class': 'form-control'}),
        }