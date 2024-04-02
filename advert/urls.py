from django.contrib import admin
from django.urls import path
from advert import views  
urlpatterns = [
    path('advert/', views.advert_list),
    path('advert/<int:pk>/', views.advert_detail),
]