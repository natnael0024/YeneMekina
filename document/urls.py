from django.urls import path
from .views import (document_list_view,document_detail_view, document_image_delete)

app_name = 'document'

urlpatterns = [
    path('documents',document_list_view, name='document_list_view'),
    path('documents/<int:id>',document_detail_view, name='document_detail_view'),
    path('documents/<int:id>/images/<int:index>',document_image_delete, name='document_image_delete')
]