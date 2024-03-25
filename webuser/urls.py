from django.urls import path
from webuser import views

urlpatterns = [
   
    path('creategroup',views.create_group),
    path('getgroup',views.get_group),
    path('editgroup/<int:group_id>',views.edit_group),
    path('groups/<int:group_id>/', views.delete_group),
    path('createpermission',views.create_permission),
    path('getpermission',views.get_permission),
    path('editpermission/<int:permission_id>',views.edit_permission),
    path('display',views.admin_view),
]