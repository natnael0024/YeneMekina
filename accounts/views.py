from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer
from django.contrib.auth import authenticate
from .serializers import UserSerializer
from django.contrib.auth.models import Group # Import your user serializer



class UserRegistrationView(APIView):
    def post(self, request):
        group_id = request.data.get('group')
        
        try:
            group = Group.objects.get(id=group_id)
        except Group.DoesNotExist:
            return Response({'message': 'Group not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.groups.add(group)  
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
                'token': token.key,
                'user': serializer.data  # Include serialized user data in the response
            }
            return Response(response_data, status=status.HTTP_200_OK)
        
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)