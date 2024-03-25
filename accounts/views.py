from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer
from django.contrib.auth import authenticate
from .serializers import UserSerializer
from django.contrib.auth.models import Group # Import your user serializer


import time
from django.core.files.storage import default_storage
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .serializers import CustomUserSerializer
from .models import CustomUser

from rest_framework.status import HTTP_403_FORBIDDEN

class UserRegistrationView(APIView):
    def post(self, request):
        group_id = request.data.get('group')
        group = None
        
        if group_id:
            try:
                group = Group.objects.get(id=group_id)
            except Group.DoesNotExist:
                return Response({'message': 'Group not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            if group:
                user.groups.add(group)
            else:
                default_group = Group.objects.get(name='user')  # Replace 'default' with the name of your default group
                user.groups.add(default_group)

            token, _ = Token.objects.get_or_create(user=user)
            return Response({'user': serializer.data}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class UserLoginView(APIView):
    def post(self, request):
        phone_number = request.data.get('phone_number')
        password = request.data.get('password')
        user = authenticate(username=phone_number, password=password)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            serializer = UserSerializer(user)  # Serialize the user object
            response_data = {
                "token": token.key,
                "user": serializer.data,  # Include serialized user data in the response
            }
            return Response(response_data, status=status.HTTP_200_OK)
        return Response(
            {"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
        )
@csrf_exempt
@api_view(['PUT'])
def update_profile(request):
    token = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[1]
    try:
        token_obj = Token.objects.get(key=token)
        user = token_obj.user
    except Token.DoesNotExist:
        user = None
    if user:
        user_id = user.id
    else:
        return Response({'message: unauthenticated'})
    user = get_object_or_404(CustomUser, id=user_id)
    serializer = CustomUserSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        if request.FILES.get('avatar'):
            avatar = request.FILES['avatar']
            if user.avatar:
                # Delete the existing avatar file
                default_storage.delete(user.avatar.path)
            # Save the new avatar file
            avatar_name = f'avatar_{user.first_name}_{int(time.time())}.{avatar.name.split(".")[-1]}'
            avatar_path = default_storage.save(f'{settings.MEDIA_ROOT}/avatars/{avatar_name}', avatar)
            user.avatar = avatar_path
            user.save()
        return JsonResponse(serializer.data)
    return JsonResponse(serializer.errors, status=400)