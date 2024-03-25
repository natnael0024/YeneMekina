from django.urls import path
from .views import UserRegistrationView, UserLoginView
from .views import update_profile
app_name = 'accounts'

urlpatterns = [
   path('api/user/register', UserRegistrationView.as_view(), name='register'),
   path('api/login', UserLoginView.as_view(), name='login'),
   path('api/user/update', update_profile, name='update_profile'), 
]
