from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from rest_framework.decorators import api_view,permission_classes,authentication_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rest_framework import permissions
from django.contrib.auth.models import Group,Permission
from .permissions import IsAdminUser
from django.contrib.contenttypes.models import ContentType


@api_view(['POST'])
def create_group(request):
    group_name = request.data.get('group_name')
    if group_name:
        group = Group(name=group_name)
        group.save()
        return Response({'message': 'Group created successfully.'})

    return Response({'error': 'Group name is required.'}, status=400)

@api_view(['GET'])
def get_group(request):
    groups = Group.objects.all().values('id', 'name')
    return Response({'groups': groups})

@api_view(['PUT'])
def edit_group(request, group_id):
    permission_ids = request.data.get('permission_ids', [])
    group_name = request.data.get('group_name')
    
    try:
        group = Group.objects.get(id=group_id)
    except Group.DoesNotExist:
        return Response({'error': 'Group not found.'}, status=404)

    if group_name:
        group.name = group_name
    
    if permission_ids:
        try:
            permissions = Permission.objects.filter(id__in=permission_ids)
            group.permissions.set(permissions)
        except Permission.DoesNotExist:
            return Response({'error': 'permissions do not exist.'}, status=400)
    
    group.save()
    return Response({'message': 'Group updated successfully.'})
@api_view(['DELETE'])
def delete_group(request, group_id):
    group = Group.objects.get(id=group_id)
    group.delete()
    return Response({'message': 'Group deleted successfully.'})

@api_view(['POST'])
def create_permission(request):
    
    name = request.data.get('name')

    if not all([name]):
        return Response({'error': 'Missing required fields.'}, status=400)

    try:
        content_type = ContentType.objects.get_for_model(Group)
        permission = Permission.objects.create(
            
            name=name,
            content_type=content_type,
        )
    except Exception as e:
        return Response({'error': str(e)}, status=500)

    return Response({'message': 'Permission created successfully.'})

@api_view(['GET'])
def get_permission(request):
    permissions = Permission.objects.all().values('id','name')
    return Response({ 'permissions': permissions})

@api_view(['PUT'])
def edit_permission(request, permission_id):
    name = request.data.get('name')

    if not all([name]):
        return Response({'error': 'Missing required fields.'}, status=400)

    try:
        permission = Permission.objects.get(id=permission_id)
        permission.name = name
        permission.save()
    except Permission.DoesNotExist:
        return Response({'error': 'Permission not found.'}, status=404)
    except Exception as e:
        return Response({'error': str(e)}, status=500)

    return Response({'message': 'Permission updated successfully.'})


@api_view(['GET'])
@permission_classes([IsAuthenticated,IsAdminUser])
def admin_view(request):
    return Response({'message': 'hello admin'})





