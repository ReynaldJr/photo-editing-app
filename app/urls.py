from django.urls import path
from app import views

urlpatterns = [
    path("<int:id>", views.edit, name="edit"),
    path("", views.upload, name="upload"),
    path("upload_unsplash", views.upload_unsplash, name="upload_unsplash"),
]
