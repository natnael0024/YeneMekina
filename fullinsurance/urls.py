from django.urls import path
from .views import (
    fullinsurance_list_view,
    fullinsurance_detail_view,
    fullinsurance_image_delete
)
urlpatterns = [
    path('fullinsurances',fullinsurance_list_view,name='fullinsurance_list_view'),
    path('fullinsurances/<int:id>',fullinsurance_detail_view,name='fullinsurance_detail_view'),
    path('fullinsurances/<int:id>/images/<int:index>',fullinsurance_image_delete, name='fullinsurance_image_delete')
]
