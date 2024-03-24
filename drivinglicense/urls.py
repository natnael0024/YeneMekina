from django.urls import path
from .views import (
    driving_license_list,
    # driving_license_create,
    driving_license_detail,
    # driving_license_update,
    # driving_license_delete,
)

urlpatterns = [
    path('drivinglicenses', driving_license_list, name='driving_license_list'),
    # path('drivinglicenses/create', driving_license_create, name='driving_license_create'),
    path('drivinglicenses/<int:id>', driving_license_detail, name='driving_license_detail'),
    # path('drivinglicenses/<int:id>', driving_license_update, name='driving_license_update'),
    # path('drivinglicenses/<int:id>', driving_license_delete, name='driving_license_delete'),
]