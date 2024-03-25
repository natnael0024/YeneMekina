from django.urls import path
from .views import (
    fullinsurance_list_view,
    fullinsurance_detail_view
)
urlpatterns = [
    path('fullinsurances',fullinsurance_list_view,name='fullinsurance_list_view'),
    path('fullinsurances/<int:id>',fullinsurance_detail_view,name='fullinsurance_detail_view'),
]
