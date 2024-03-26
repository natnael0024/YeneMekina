from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import FullInsurance
from bolo.models import Bolo
from roadfund.models import RoadFund
from thirdparty.models import ThirdParty
from oilservice.models import OilService
from .serializers import FullInsuranceSerializer
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404
from django.core.files.storage import default_storage
from django.conf import settings
import os
import uuid
import json

@api_view(['GET','POST'])
def fullinsurance_list_view(request):

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
        full_insurances = FullInsurance.objects.filter(vehicle__user=user).order_by('-created_at')

        serialized_data = []
        for full_insurance in full_insurances:
            full_insurance_data = FullInsuranceSerializer(full_insurance).data
            if full_insurance.images:
                images = json.loads(full_insurance.images)
                images_data = [{'index': index, 'image': image} for index, image in enumerate(images)]
                full_insurance_data['images'] = images_data
            serialized_data.append(full_insurance_data)

        return Response({'date':serialized_data}, status=status.HTTP_200_OK)
    
    # create
    elif request.method == 'POST':
        plate_number = request.POST.get('plate_number')

        images = []
        if 'images' in request.FILES:
            for image in request.FILES.getlist('images'):
                file_ext = os.path.splitext(image.name)[1]
                image_name = f'fullinsurance_{uuid.uuid4()}{file_ext}'
                file_path = f'fullinsurances/{image_name}'
                default_storage.save(file_path, image)
                image_url = f'{settings.MEDIA_URL}{file_path}'
                images.append(image_url)

        vehicle = user.vehicles.filter(plate_number=plate_number).first()

        if vehicle:
            if vehicle.full_insurances.count() > 0:
                return Response({'message': 'Full insurance already registered for this plate'}, status=409)
        else:
            vehicle = user.vehicles.create(plate_number=plate_number)

        if vehicle.bolos.count() < 1:
            Bolo.objects.create(vehicle=vehicle)
        if vehicle.road_funds.count() < 1:
            RoadFund.objects.create(vehicle=vehicle)
        if vehicle.third_parties.count() < 1:
            ThirdParty.objects.create(vehicle=vehicle)
        if vehicle.oil_services.count() < 1:
            OilService.objects.create(vehicle=vehicle)

        full_insurance = FullInsurance.objects.create (
            vehicle_id = vehicle.id,
            insurer = request.data.get('insurer'),
            issue_date= request.data.get('issue_date'),
            expire_date = request.data.get('expire_date'),
            images = json.dumps(images),
            notification_status = False
        )

        images = json.loads(full_insurance.images)
        images_data = [{'index': index, 'image': image} for index, image in enumerate(images)]
        full_insurance_data = FullInsuranceSerializer(full_insurance).data
        full_insurance_data['images'] = images_data

        return Response(full_insurance_data, status=status.HTTP_201_CREATED)
    
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)



@api_view(['GET','POST','PUT','DELETE'])
def fullinsurance_detail_view(request,id):
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
    
    full_insurance = get_object_or_404(FullInsurance, id=id,vehicle__user=user)

    #show
    if request.method == 'GET':
        images = json.loads(full_insurance.images)
        images_data = [{'index': index, 'image': image} for index, image in enumerate(images)]
        serialized = FullInsuranceSerializer(full_insurance).data
        serialized['images'] = images_data

        return Response({'data':serialized})
    
    #update
    elif request.method == 'POST' or request.method == 'PUT':
        plate_number = request.data.get('plate_number')
        insurer = request.data.get('insurer')
        issue_date = request.data.get('issue_date')
        expire_date = request.data.get('expire_date')

        if plate_number:
            current_vehicle_id = full_insurance.vehicle_id

            vehicle = user.vehicles.filter(plate_number=plate_number).first()

            if vehicle:
                if vehicle.full_insurances.count() > 0:
                    return Response({'message': 'Full insurance already registered for this plate'}, status=409)
                full_insurance.vehicle_id = vehicle.id
            else:
                vehicle = user.vehicles.create(plate_number=plate_number)
                full_insurance.vehicle_id = vehicle.id

            # update other docs
            bolo = Bolo.objects.filter(vehicle_id=current_vehicle_id).first()
            if bolo:
                bolo.vehicle_id = full_insurance.vehicle_id
                bolo.save()
            rf = RoadFund.objects.filter(vehicle_id=current_vehicle_id).first()
            if rf:
                rf.vehicle_id = full_insurance.vehicle_id
                rf.save()
            tp = ThirdParty.objects.filter(vehicle_id=current_vehicle_id).first()
            if tp:
                tp.vehicle_id = full_insurance.vehicle_id
                tp.save()
            oi = OilService.objects.filter(vehicle_id=current_vehicle_id).first()
            if oi:
                oi.vehicle_id = full_insurance.vehicle_id
                oi.save()

        if insurer:
            full_insurance.insurer = insurer
        if issue_date:
            full_insurance.issue_date = issue_date
        if expire_date:
            full_insurance.expire_date = expire_date

        if 'images' in request.FILES :
            new_images = []
            for image in request.FILES.getlist('images'):
                file_ext = os.path.splitext(image.name)[1]
                image_name = f'fullinsurance_{uuid.uuid4()}{file_ext}'
                file_path = f'fullinsurances/{image_name}'
                default_storage.save(file_path, image)
                image_url = f'{settings.MEDIA_URL}{file_path}'
                new_images.append(image_url)
             # Update Images
            images = json.loads(full_insurance.images)
            images.extend(new_images)
            full_insurance.images = json.dumps(images)

        full_insurance.save()

        images = json.loads(full_insurance.images)
        images_data = [{'index': index, 'image': image} for index, image in enumerate(images)]
        serialized = FullInsuranceSerializer(full_insurance).data
        serialized['images'] = images_data

        return Response({'data':serialized},status=200)

    elif request.method == 'DELETE':
        if full_insurance.images:
            images = json.loads(full_insurance.images)
            for image_url in images:
                # Extract file path from image URL
                file_path = image_url.replace(settings.MEDIA_URL, '')
                # Delete the image file from storage
                if default_storage.exists(file_path):
                    default_storage.delete(file_path)

        full_insurance.delete()
        return Response(status=204)
    
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['DELETE'])
def fullinsurance_image_delete(request,id,index):
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

    full_insurance = get_object_or_404(FullInsurance, id=id, vehicle__user=user)

    if request.method == 'DELETE':
        if full_insurance.images:
            images = json.loads(full_insurance.images)

            if 0 <= index < len(images):
                # Extract the file path of the image to be deleted
                image_url_to_delete = images[index]
                file_path_to_delete = image_url_to_delete.replace(settings.MEDIA_URL, '')

                # Delete the image file from storage
                if default_storage.exists(file_path_to_delete):
                    default_storage.delete(file_path_to_delete)

                # Remove the image URL from the list of images
                del images[index]
                full_insurance.images = json.dumps(images)
                full_insurance.save()

                return Response({'message': 'Image at index {} deleted successfully'.format(index)}, status=200)
            else:
                return Response({'message': 'Invalid index provided'}, status=400)
        else:
            return Response({'message': 'No images to delete'}, status=404)
        
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

