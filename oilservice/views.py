from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import OilService
from bolo.models import Bolo
from roadfund.models import RoadFund
from thirdparty.models import ThirdParty
from fullinsurance.models import FullInsurance
from vehicle.models import Vehicle
from .serializers import OilServiceSerializer
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404
import os
import uuid
import json

@api_view(['GET','POST'])
def oilservice_list_view(request):
    token = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[1]
    try:
        token_obj = Token.objects.get(key=token)
        user = token_obj.user
    except Token.DoesNotExist:
        user = None

    if user:
        user_id = user.id
    else:
        return Response('message: unauthenticated')
    
    if request.method == 'GET':
        oil_services = OilService.objects.filter(vehicle__user_id=user_id).order_by('-created_at')
        serializer = OilServiceSerializer(oil_services,many=True)
        return Response({'data':serializer.data})
    
    # create new oil service
    elif request.method == 'POST':
        plate_number = request.data.get('plate_number')
        next_service_date = request.data.get('next_service_date')
        fill_date = request.data.get('fill_date')
        expire_date = request.data.get('expire_date')

        vehicle = Vehicle.objects.filter(user=user, plate_number=plate_number).first()

        if vehicle:
            oil_service_count = vehicle.oil_services.count()
            if oil_service_count > 0:
                return Response({'message': 'Oil service date already registered for this plate'}, status=409)
        else:
            vehicle = Vehicle.objects.create(user=user, plate_number=plate_number)
        
        if vehicle.bolos.count() < 1:
            Bolo.objects.create(vehicle=vehicle)
        if vehicle.full_insurances.count() < 1:
            FullInsurance.objects.create(vehicle=vehicle, images=json.dumps([]))
        if vehicle.third_parties.count() < 1:
            ThirdParty.objects.create(vehicle=vehicle)
        if vehicle.road_funds.count() < 1:
            RoadFund.objects.create(vehicle=vehicle)

        oil_service = OilService.objects.create(
            vehicle_id = vehicle.id,
            fill_date = fill_date,
            next_service_date = next_service_date,
            expire_date = expire_date,
            notification_status=False
        )

        serializer = OilServiceSerializer(oil_service)
        return Response({'data':serializer.data}, status=201)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

# show, update, delete
@api_view(['GET','PUT','POST','DELETE'])
def oilservice_detail_view(request,id):
    token = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[1]
    try:
        token_obj = Token.objects.get(key=token)
        user = token_obj.user
    except Token.DoesNotExist:
        user = None

    if user:
        user_id = user.id
    else:
        return Response('message: unauthenticated')
    
    oil_service = get_object_or_404(OilService,id=id, vehicle__user = user)

    #show
    if request.method == 'GET':
        serializer = OilServiceSerializer(oil_service)
        return Response({'data':serializer.data})
    
    # update
    if request.method == 'POST' or request.method == 'PUT':
        plate_number = request.data.get('plate_number')
        fill_date = request.data.get('fill_date')
        expire_date = request.data.get('expire_date')
        next_service_date = request.data.get('next_service_date')
        
        if plate_number:
            current_vehicle_id = oil_service.vehicle_id

            vehicle = Vehicle.objects.filter(plate_number=plate_number, user=user).first()

            if vehicle:
                oil_service_count = vehicle.oil_services.count()
                if oil_service_count > 0 :
                    return Response({'message': 'Oil service date already registered for this plate'}, status=409)
                oil_service.vehicle_id = vehicle.id
                
            else:
                vehicle = Vehicle.objects.create(plate_number=plate_number, user=user)
                oil_service.vehicle_id = vehicle.id

            # update other docs
            bolo = Bolo.objects.filter(vehicle_id=current_vehicle_id).first()
            if bolo:
                bolo.vehicle_id = oil_service.vehicle_id
                bolo.save()
            fi = FullInsurance.objects.filter(vehicle_id=current_vehicle_id).first()
            if fi:
                fi.vehicle_id = oil_service.vehicle_id
                fi.save()
            tp = ThirdParty.objects.filter(vehicle_id=current_vehicle_id).first()
            if tp:
                tp.vehicle_id = oil_service.vehicle_id
                tp.save()
            rf = RoadFund.objects.filter(vehicle_id=current_vehicle_id).first()
            if rf:
                rf.vehicle_id = oil_service.vehicle_id
                rf.save()


        if fill_date:
            oil_service.fill_date = fill_date
        if expire_date:
            oil_service.expire_date = expire_date
        if next_service_date:
            oil_service.next_service_date = next_service_date
        oil_service.save()

        serializer = OilServiceSerializer(oil_service)

        return Response({'data':serializer.data}, status=200)
    
    #delete
    elif request.method == 'DELETE':
        oil_service.delete()
        return Response(status=204)
    
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
