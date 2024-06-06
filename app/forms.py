from django import forms
from .models import Photo

class EditPhotoUpload(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['image', 'name']
        
    
        