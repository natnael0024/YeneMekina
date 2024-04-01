from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Document
from .serializers import DocumentSerializer
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404
from django.core.files.storage import default_storage
from django.conf import settings
import os
import uuid
import json
from django.http import JsonResponse
# Create your views here.

@api_view(['GET','POST'])
def document_list_view(request):
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

    if request.method == 'GET':
        documents = Document.objects.filter(user=user).order_by('-created_at')

        # serialized_data = []
        # for doc in documents:
        #     doc_data = DocumentSerializer(doc).data
        #     if doc.images:
        #         images = json.loads(doc.images)
        #         images_data = [{'index': index, 'image': image} for index, image in enumerate(images)]
        #         doc_data['images'] = images_data
        #     serialized_data.append(doc_data)

        grouped_documents = []
        for document in documents:
            date_str = document.created_at.date().isoformat()
            # if date_str not in grouped_documents:
            #     grouped_documents[date_str] = []
        
            images = []
            for index, image in enumerate(document.images):
                images = json.loads(document.images)
                images_data = [{'index': index, 'image': image, 'document_id': document.id} for index, image in enumerate(images)]
                # images.append({
                #     'document_id': document.id,
                #     'index': index,
                #     'image': images_data
                # })
        
            grouped_documents.append({
                'date': date_str,
                'images': images_data
            })

        return Response({'data':grouped_documents}, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        images = []
        if 'images' in request.FILES:
            for image in request.FILES.getlist('images'):
                file_ext = os.path.splitext(image.name)[1]
                image_name = f'document_{uuid.uuid4()}{file_ext}'
                file_path = f'documents/{image_name}'
                default_storage.save(file_path, image)
                image_url = f'{settings.MEDIA_URL}{file_path}'
                images.append(image_url)
        
        document = Document.objects.create(
            user = user,
            images = json.dumps(images)
        )

        images = json.loads(document.images)
        images_data = [{'index': index, 'image': image} for index, image in enumerate(images)]
        serialized = DocumentSerializer(document).data
        serialized['images'] = images_data

        return Response({'data':serialized},status=201)

    return Response(status=405)

@api_view(['GET','POST','PUT','DELETE'])
def document_detail_view(request, id):
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

    document = get_object_or_404(Document,id=id, user=user)

    if request.method == 'GET':
        images = json.loads(document.images)
        images_data = [{'index': index, 'image': image} for index, image in enumerate(images)]
        serialized = DocumentSerializer(document).data
        serialized['images'] = images_data
        return Response({'data':serialized},status=200)

    elif request.method == 'PUT' or request.method == 'POST':
        if 'images' in request.FILES :
            new_images = []
            for image in request.FILES.getlist('images'):
                file_ext = os.path.splitext(image.name)[1]
                image_name = f'document_{uuid.uuid4()}{file_ext}'
                file_path = f'documents/{image_name}'
                default_storage.save(file_path, image)
                image_url = f'{settings.MEDIA_URL}{file_path}'
                new_images.append(image_url)
             # Update Images
            images = json.loads(document.images)
            images.extend(new_images)
            document.images = json.dumps(images)

        document.save()

        images = json.loads(document.images)
        images_data = [{'index': index, 'image': image} for index, image in enumerate(images)]
        serialized = DocumentSerializer(document).data
        serialized['images'] = images_data

        return Response({'data':serialized},status=200)

    elif request.method == 'DELETE':
        if document.images:
            images = json.loads(document.images)
            for image_url in images:
                # Extract file path from image URL
                file_path = image_url.replace(settings.MEDIA_URL, '')
                # Delete the image file from storage
                if default_storage.exists(file_path):
                    default_storage.delete(file_path)

        document.delete()
        return Response(status=204)


@api_view(['DELETE'])
def document_image_delete(request,id,index):
    token = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[1]
    try:
        token_obj = Token.objects.get(key=token)
        user = token_obj.user
    except Token.DoesNotExist:
        user = None

    if user:
        user_id = user.id
    else:
        return Response({'message': 'Unauthenticated'}, status=401)

    document = get_object_or_404(Document, id=id, user=user)

    if request.method == 'DELETE':
        if document.images:
            images = json.loads(document.images)

            if 0 <= index < len(images):
                # Extract the file path of the image to be deleted
                image_url_to_delete = images[index]
                file_path_to_delete = image_url_to_delete.replace(settings.MEDIA_URL, '')

                # Delete the image file from storage
                if default_storage.exists(file_path_to_delete):
                    default_storage.delete(file_path_to_delete)

                # Remove the image URL from the list of images
                del images[index]
                document.images = json.dumps(images)
                document.save()

                return Response({'message': 'Image at index {} deleted successfully'.format(index)}, status=200)
            else:
                return Response({'message': 'Invalid index provided'}, status=400)
        else:
            return Response({'message': 'No images to delete'}, status=404)
        
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

