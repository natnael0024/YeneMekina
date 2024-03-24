from django.urls import path
from .views import (
    thirdparty_list_view,
    thirdParty_detail_view
)

urlpatterns = [
    path('thirdparties',thirdparty_list_view, name='thirdparty_list_view'),
    path('thirdparties/<int:id>',thirdParty_detail_view, name='thirdparty_detail_view'),
]
