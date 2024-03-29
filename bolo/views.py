from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from webuser.permissions import IsAdminUser
from .models import Bolo
from thirdparty.models import ThirdParty
from roadfund.models import RoadFund
from fullinsurance.models import FullInsurance
from oilservice.models import OilService
from .serializers import BoloSerializer
from vehicle.models import Vehicle
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.db.models import Count
import json
import os
import uuid


@api_view(['GET','POST'])
def bolo_list_view(request):

    token = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[1]
    try:
        token_obj = Token.objects.get(key=token)
        user = token_obj.user
    except Token.DoesNotExist:
    # Handle the case when the token does not exist or is invalid
        user = None

    if user:
        user_id = user.id
    # Continue with your logic using the user ID
    else:
    # Handle the case when the token is invalid or the user does not exist
        return Response({'message: unauthenticated'})
    
    if request.method == 'GET':
        bolos = Bolo.objects.filter(vehicle__user_id=user_id).order_by('-created_at')
        serializer = BoloSerializer(bolos, many=True)
        return Response({'data':serializer.data}, status=200)
    
    # create new bolo
    elif request.method == 'POST':
        plate_number = request.POST.get('plate_number')
        inspection_date = request.POST.get('inspection_date')
        expire_date = request.POST.get('expire_date')
        image = request.FILES.get('image')

        if image:
            file_ext = os.path.splitext(image.name)[1]
            new_file_name = f'bolo_{uuid.uuid4()}{file_ext}'
            image.name = new_file_name
        # Validation
        # if not all([plate_number, inspection_date, expire_date]):
        #     return Response({'message': 'Missing required fields : plate_number, inspection_date, expire_date'}, status=400)

        vehicle = Vehicle.objects.filter(user=user, plate_number=plate_number).first()

        if vehicle:
            bolo_count = vehicle.bolos.count()
            if bolo_count > 0:
                return Response({'message': 'Bolo already registered for this plate'}, status=409)            
        else:
            vehicle = Vehicle.objects.create(plate_number=plate_number, user=user)

        if vehicle.road_funds.count() < 1:
            RoadFund.objects.create(vehicle=vehicle)
        if vehicle.third_parties.count() < 1:
            ThirdParty.objects.create(vehicle=vehicle)
        if vehicle.full_insurances.count() < 1:
            FullInsurance.objects.create(vehicle=vehicle, images=json.dumps([]))
        if vehicle.oil_services.count() < 1:
            OilService.objects.create(vehicle=vehicle)

        bolo = Bolo.objects.create(
            vehicle_id=vehicle.id,
            inspection_date=inspection_date,
            expire_date=expire_date,
            image=image,
            notification_status=False
        )
        serializer = BoloSerializer(bolo)
        return Response({'data':serializer.data}, status=201)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)



@api_view(['GET','POST','PUT','DELETE'])
def bolo_detail_view(request, id):
    token = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[1]
    try:
        token_obj = Token.objects.get(key=token)
        user = token_obj.user
    except Token.DoesNotExist:
    # Handle the case when the token does not exist or is invalid
        user = None

    if user:
        user_id = user.id
    # Continue with your logic using the user ID
    else:
    # Handle the case when the token is invalid or the user does not exist
        return Response({'message: unauthenticated'})
    
    bolo = get_object_or_404(Bolo, id=id, vehicle__user=user)
    if request.method == 'GET':
        serializer = BoloSerializer(bolo)
        return Response({'data':serializer.data})
    
    # update bolo
    elif request.method == 'POST' or request.method == 'PUT':
        plate_number = request.POST.get('plate_number')
        inspection_date = request.POST.get('inspection_date')
        expire_date = request.POST.get('expire_date')
        image = request.FILES.get('image')

        if plate_number is not None and plate_number != '':
            current_vehicle_id = bolo.vehicle_id

            vehicle = Vehicle.objects.filter(user=user, plate_number=plate_number).first()

            if vehicle:
                bolo_exist = Bolo.objects.filter(vehicle_id=vehicle.id).exclude(id=id).exists()

                if bolo_exist:
                    return Response({'message': 'Bolo already exists for this plate'}, status=409)

                bolo.vehicle_id = vehicle.id
            else:
                vehicle = Vehicle.objects.create(user=user, plate_number=plate_number)
                bolo.vehicle_id = vehicle.id

            rf = RoadFund.objects.filter(vehicle_id=current_vehicle_id).first()
            if rf:
                rf.vehicle_id = bolo.vehicle_id
                rf.save()

            fi = FullInsurance.objects.filter(vehicle_id=current_vehicle_id).first()
            if fi:
                fi.vehicle_id = bolo.vehicle_id
                fi.save()

            tp = ThirdParty.objects.filter(vehicle_id=current_vehicle_id).first()
            if tp:
                tp.vehicle_id = bolo.vehicle_id
                tp.save()
            oi = OilService.objects.filter(vehicle_id=current_vehicle_id).first()
            if oi:
                oi.vehicle_id = bolo.vehicle_id
                oi.save()

        if image:
            if bolo.image:
                bolo.image.delete()    
            file_ext = os.path.splitext(image.name)[1]
            new_file_name = f'bolo_{uuid.uuid4()}{file_ext}'
            image.name = new_file_name
            bolo.image = image

        if inspection_date:
            bolo.inspection_date = inspection_date

        if expire_date:
            bolo.expire_date = expire_date

        bolo.save()
        serializer = BoloSerializer(bolo)
        return Response({'data':serializer.data})
    
    #delete
    elif request.method == 'DELETE':
        if bolo.image:
            bolo.image.delete()
        bolo.delete()
        return Response({}, status=204)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)