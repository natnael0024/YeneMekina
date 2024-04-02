from django.contrib import admin
from django.urls import path
from map import views  
urlpatterns = [
    path('article/', views.article_list),
    path('article/<int:pk>/', views.article_detail),
    path('map/',views.map_store),
]