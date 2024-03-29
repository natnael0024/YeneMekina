from django.urls import path
from .views import (oilservice_list_view, oilservice_detail_view)

urlpatterns = [
    path('oils', oilservice_list_view, name='oilservice_list_view'),
    path('oils/<int:id>', oilservice_detail_view, name='oilservice_detail_view'),
]
