from django.urls import path
from .views import (roadfund_list_view,
                    roadfund_detail_view)

urlpatterns = [
    path('roadfunds',roadfund_list_view, name='roadfund_list_view'),
    path('roadfunds/<int:id>', roadfund_detail_view, name='roadfund_detail_view')
]
