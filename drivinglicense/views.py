from django.shortcuts import render

# Create your views here.
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import DrivingLicense
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from .serializers import DrivingLicenseSerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
import os
import uuid

@api_view(['GET','POST'])
def driving_license_list(request):
    token = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[1]
    try:
        token_obj = Token.objects.get(key=token)
        user = token_obj.user
    except Token.DoesNotExist:
        user = None

    if user:
        user_id = user.id
    else:
        return JsonResponse('message: unauthenticated')
    
    if request.method == 'GET':
        driving_licenses = DrivingLicense.objects.filter(user=user).order_by('-id')
        serializer = DrivingLicenseSerializer(driving_licenses, many=True)
        return Response({'data':serializer.data})
    
    #create
    elif request.method == 'POST':
        if request.FILES.get('image'):
            file_ext = os.path.splitext(request.FILES.get('image').name)[1]
            request.FILES.get('image').name = f'license_{uuid.uuid4()}{file_ext}'
        serializer = DrivingLicenseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=user)
            return Response({'data':serializer.data}, status=201)
        return Response(serializer.errors, status=400)
    
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def driving_license_detail(request, id):
    token = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[1]
    try:
        token_obj = Token.objects.get(key=token)
        user = token_obj.user
    except Token.DoesNotExist:
        user = None

    if user:
        user_id = user.id
    else:
        return JsonResponse('message: unauthenticated')
    
    if request.method == 'GET':
        driving_license = get_object_or_404(DrivingLicense, id=id, user=user)
        serializer = DrivingLicenseSerializer(driving_license)
        return Response({'data':serializer.data})
    
    #update
    elif request.method == 'POST' or request.method == 'PUT':
        driving_license = get_object_or_404(DrivingLicense, id=id, user=user)
        if request.FILES.get('image'):
            if driving_license.image:
                driving_license.image.delete()
            file_ext = os.path.splitext(request.FILES.get('image').name)[1]
            request.FILES.get('image').name = f'license_{uuid.uuid4()}{file_ext}'
        serializer = DrivingLicenseSerializer(driving_license, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    
    #delete
    elif request.method == 'DELETE':
        driving_license = get_object_or_404(DrivingLicense, id=id, user=user)
        if driving_license.image:
            driving_license.image.delete()
        driving_license.delete()
        return Response(status=204)
    
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)