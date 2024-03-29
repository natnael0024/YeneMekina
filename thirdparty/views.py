from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import ThirdParty
from bolo.models import Bolo
from roadfund.models import RoadFund
from fullinsurance.models import FullInsurance
from oilservice.models import OilService
from vehicle.models import Vehicle
from .serializers import ThirdPartySerializer
from rest_framework.authtoken.models import Token
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
import os
import uuid
import json

@api_view(['GET','POST'])
def thirdparty_list_view(request):
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
        thirdparties = ThirdParty.objects.filter(vehicle__user_id=user_id).order_by('-created_at')
        serializer = ThirdPartySerializer(thirdparties,many=True)
        return Response({'data':serializer.data}, status=200)
    
    # create new ThirdParty
    elif request.method == 'POST':
        plate_number = request.POST.get('plate_number')
        insurer = request.POST.get('insurer')
        issue_date = request.POST.get('issue_date')
        expire_date = request.POST.get('expire_date')
        image = request.FILES.get('image')

        if image:
            file_ext = os.path.splitext(image.name)[1]
            image.name = f'thirdparty_{uuid.uuid4()}{file_ext}'

        vehicle = Vehicle.objects.filter(user=user, plate_number=plate_number).first()

        if vehicle:
            thirdparty_count = vehicle.third_parties.count()
            if thirdparty_count > 0:
                return Response({'message': 'Third Party insurance already registered for this plate'}, status=409)
        else:
            vehicle = Vehicle.objects.create(user=user, plate_number=plate_number)
            
        if vehicle.bolos.count() < 1:
            Bolo.objects.create(vehicle=vehicle)
        if vehicle.full_insurances.count() < 1:
            FullInsurance.objects.create(vehicle=vehicle, images=json.dumps([]))
        if vehicle.road_funds.count() < 1:
            RoadFund.objects.create(vehicle=vehicle)
        if vehicle.oil_services.count() < 1:
            OilService.objects.create(vehicle=vehicle)

        thirdparty = ThirdParty.objects.create(
            vehicle_id = vehicle.id,
            issue_date = issue_date,
            expire_date = expire_date,
            insurer = insurer,
            image = image,
            notification_status=False
        )

        serializer = ThirdPartySerializer(thirdparty)
        return Response(serializer.data, status=201)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

# show, update, delete
@api_view(['GET','PUT','POST','DELETE'])
def thirdParty_detail_view(request,id):
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
    
    thirdparty = get_object_or_404(ThirdParty,id=id, vehicle__user = user)

    #show
    if request.method == 'GET':
        serializer = ThirdPartySerializer(thirdparty)
        return Response({'data':serializer.data})
    
    # update
    if request.method == 'POST' or request.method == 'PUT':
        plate_number = request.POST.get('plate_number')
        issue_date = request.POST.get('issue_date')
        expire_date = request.POST.get('expire_date')
        insurer = request.POST.get('insurer')
        image = request.FILES.get('image')

        if image:
            if thirdparty.image:
                thirdparty.image.delete()
            file_ext = os.path.splitext(image.name)[1]
            image.name = f'thirdparty_{uuid.uuid4()}{file_ext}'
            thirdparty.image = image
        
        if plate_number:
            current_vehicle_id = thirdparty.vehicle_id

            vehicle = Vehicle.objects.filter(plate_number=plate_number, user=user).first()

            if vehicle:
                thirdparty_count = vehicle.third_parties.count()
                if thirdparty_count > 0 :
                    return Response({'message': 'Third Party Insurance already registered for this plate'}, status=409)
                thirdparty.vehicle_id = vehicle.id
                
            else:
                vehicle = Vehicle.objects.create(plate_number=plate_number, user=user)
                thirdparty.vehicle_id = vehicle.id


            # update other docs
            bolo = Bolo.objects.filter(vehicle_id=current_vehicle_id).first()
            if bolo:
                bolo.vehicle_id = thirdparty.vehicle_id
                bolo.save()
            rf = RoadFund.objects.filter(vehicle_id=current_vehicle_id).first()
            if rf:
                rf.vehicle_id = thirdparty.vehicle_id
                rf.save()
            fi = FullInsurance.objects.filter(vehicle_id=current_vehicle_id).first()
            if fi:
                fi.vehicle_id = thirdparty.vehicle_id
                fi.save()
            oi = OilService.objects.filter(vehicle_id=current_vehicle_id).first()
            if oi:
                oi.vehicle_id = thirdparty.vehicle_id
                oi.save()
            

        if issue_date:
            thirdparty.issue_date = issue_date
        if expire_date:
            thirdparty.expire_date = expire_date
        if insurer:
            thirdparty.insurer = insurer
        thirdparty.save()
        serializer = ThirdPartySerializer(thirdparty)

        return Response({'data':serializer.data}, status=200)
    
    #delete
    elif request.method == 'DELETE':
        if thirdparty.image:
            thirdparty.image.delete()
        thirdparty.delete()
        return Response(status=204)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

