from django.db import models
from .utils import get_filtered_image
from PIL import Image
import numpy as np
from io import BytesIO
from django.core.files.base import ContentFile
from django.contrib.auth.models import User
import os


ACTION_CHOICES = {
    ('INVERT', 'invert'), 
    ('SHARPEN', 'sharpen'), 
    ('BINARY', 'binary'), 
    ('GRAYSCALE', 'grayscale'), 
    ('BLURRED', 'blurred'), 
    ('SEPIA', 'sepia'), 
    ('SKETCH', 'sketch'), 
    ('COLORIZED', 'colorized'), 
    ('COLD', 'cold'),
    ('WARM', 'warm'),  
}

class Photo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="photo", null=True)
    image = models.ImageField(upload_to='images/')
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=300, default="")
    action = models.CharField(max_length=50, choices=ACTION_CHOICES, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    def save_edit(self, *args, **kwargs):
        # Open Image
        pil_image = Image.open(self.image)
        
        cv_img = np.array(pil_image)
        img = get_filtered_image(cv_img, self.action)
        
        im_pil = Image.fromarray(img)
        
        buffer = BytesIO()
        
        im_pil.save(buffer, format="png")
        image_png = buffer.getvalue()
        
        # Save image with the same name to avoid creating new directories
        image_name = os.path.basename(self.image.name)
        self.image.save(image_name, ContentFile(image_png), save=False)
        
        super().save(*args, **kwargs)
        