from django.urls import path
from .views import (
    thirdparty_list_view,
    thirdParty_detail_view
)

urlpatterns = [
    path('',thirdparty_list_view, name='thirdparty_list_view'),
    path('/<int:id>',thirdParty_detail_view, name='thirdparty_detail_view'),
]
