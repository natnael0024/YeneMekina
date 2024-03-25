from django.urls import path
from .views import (roadfund_list_view,
                    roadfund_detail_view)

urlpatterns = [
    path('',roadfund_list_view, name='roadfund_list_view'),
    path('/<int:id>', roadfund_detail_view, name='roadfund_detail_view')
]
