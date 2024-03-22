from django import forms
from .models import Poste, Employee


class PosteForm(forms.ModelForm):
    class Meta:
        model = Poste
        fields = '__all__'  # You can customize this based on your model fields

    # Add any additional form field customizations or validations if needed


