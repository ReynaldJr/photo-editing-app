from django.shortcuts import render, redirect
from .models import Photo
from .forms import EditPhotoUpload
from django.http import JsonResponse
import json
from django.core import serializers
from django.contrib.auth.decorators import login_required
from urllib.parse import urlparse, unquote
import requests
import os
from .helpers import search_image
from django.core.files.base import ContentFile
from PIL import Image
from io import BytesIO
from django.contrib.auth.models import User
from django.http import Http404
# Create your views here.

    

@login_required(login_url="login")
def edit(request, id):
    photo = Photo.objects.get(id = id)
    form = EditPhotoUpload(request.POST or None, request.FILES or None, instance=photo)
    
    if photo in request.user.photo.all():
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            pic_id = json.loads(request.POST.get('id'))
            action = request.POST.get('action')
            
            if pic_id is None:
                if form.is_valid():
                    obj = form.save(commit=False)
                    obj.action = action
                    obj.save_edit()
            
            else:
                obj = Photo.objects.get(id = id)
                
            obj.action = action
            obj.save_edit()
            data = serializers.serialize('json', [obj])
            return JsonResponse({'data': data})
        
        return render(request, "edit.html", {"name": photo, "photo": photo, 'form': form})
    raise Http404

@login_required(login_url="login")
def delete_photo(request, id):
    photo = Photo.objects.get(id = id)
    photo.delete()
    return redirect('upload')


@login_required(login_url="login")
def upload(request):
    photo_list = Photo.objects.all()
    form = EditPhotoUpload()
    
    if request.method == 'POST':
        form = EditPhotoUpload(request.POST or None, request.FILES or None)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.save()
            request.user.photo.add(photo)
            return redirect("edit", id = photo.id)
            
        else:
            form = EditPhotoUpload()
            
    photo_list = request.user.photo.all().order_by('-modified_date')
    return render(request, "index.html", {'form': form, 'photo_list': photo_list})

@login_required(login_url="login")
def upload_unsplash(request):
    image_data = []
    if request.method == "GET" and request.GET.get("search"):
        search_query = request.GET.get("search")
        quantity = request.GET.get("quantity")
        image_data = search_image(
            search_query=search_query,
            quantity=quantity
        )
        image_data = [images["urls"]["full"] for images in image_data["results"]]

    elif request.method == "POST":
        image_url = request.POST.get("selected_image")
        image_name = request.POST.get("image_name", "unsplash_image")
        # Download the image from the URL
        response = requests.get(image_url)
        
        image = Image.open(BytesIO(response.content))
        image_io = BytesIO()
        image.save(image_io, format='PNG')
        full_file_name = f"{image_name}.png"
        
        photo = Photo.objects.create(
            name=image_name,
            image=ContentFile(image_io.getvalue(), full_file_name)
        )
        request.user.photo.add(photo)
        return redirect('edit', id=photo.id)

    context = {"images": image_data}
    return render(request, "upload_unsplash.html", context=context)