from django.urls import path
from .views import (
    bolo_list_view,
    bolo_create_view,
    bolo_detail_view,
    bolo_update_view,
    bolo_delete_view,
)

app_name = 'bolos'

urlpatterns = [
    path('bolos/', bolo_list_view, name='bolo-list'),
    path('bolos', bolo_create_view, name='bolo-create'),
    path('bolos/<int:id>/', bolo_detail_view, name='bolo-detail'),
    path('bolos/<int:id>/update', bolo_update_view, name='bolo-update'),
    path('bolos/<int:id>/delete', bolo_delete_view, name='bolo-delete'),
]