from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import RoadFund
from bolo.models import Bolo
from thirdparty.models import ThirdParty
from fullinsurance.models import FullInsurance
from vehicle.models import Vehicle
from .serializers import RoadFundSerializer
from rest_framework.authtoken.models import Token
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
import os
import uuid
import json

@api_view(['GET','POST'])
def roadfund_list_view(request):
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
        roadfunds = RoadFund.objects.filter(vehicle__user_id=user_id).order_by('-created_at')
        serializer = RoadFundSerializer(roadfunds,many=True)
        return JsonResponse({'data':serializer.data}, safe=False)
    
    # create new roadfund
    elif request.method == 'POST':
        plate_number = request.POST.get('plate_number')
        issue_date = request.POST.get('issue_date')
        expire_date = request.POST.get('expire_date')
        image = request.FILES.get('image')

        if image:
            file_ext = os.path.splitext(image.name)[1]
            image.name = f'roadfund_{uuid.uuid4()}{file_ext}'

        vehicle = Vehicle.objects.filter(user=user, plate_number=plate_number).first()

        if vehicle:
            roadfund_count = vehicle.road_funds.count()
            if roadfund_count > 0:
                return JsonResponse({'message': 'Road fund already registered for this plate'}, status=409)
        else:
            vehicle = Vehicle.objects.create(user=user, plate_number=plate_number)
        
        if vehicle.bolos.count() < 1:
            Bolo.objects.create(vehicle=vehicle)
        if vehicle.full_insurances.count() < 1:
            FullInsurance.objects.create(vehicle=vehicle, images=json.dumps([]))
        if vehicle.third_parties.count() < 1:
            ThirdParty.objects.create(vehicle=vehicle)

        roadfund = RoadFund.objects.create(
            vehicle_id = vehicle.id,
            issue_date = issue_date,
            expire_date = expire_date,
            image = image,
            notification_status=False
        )

        serializer = RoadFundSerializer(roadfund)
        return JsonResponse(serializer.data, status=201)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

# show, update, delete
@api_view(['GET','PUT','POST','DELETE'])
def roadfund_detail_view(request,id):
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
    
    roadfund = get_object_or_404(RoadFund,id=id, vehicle__user = user)

    #show
    if request.method == 'GET':
        serializer = RoadFundSerializer(roadfund)
        return Response({'data':serializer.data})
    
    # update
    if request.method == 'POST' or request.method == 'PUT':
        plate_number = request.POST.get('plate_number')
        issue_date = request.POST.get('issue_date')
        expire_date = request.POST.get('expire_date')
        image = request.FILES.get('image')

        if image:
            if roadfund.image:
                roadfund.image.delete()
            file_ext = os.path.splitext(image.name)[1]
            image.name = f'roadfund_{uuid.uuid4()}{file_ext}'
            roadfund.image = image
        
        if plate_number:
            current_vehicle_id = roadfund.vehicle_id

            vehicle = Vehicle.objects.filter(plate_number=plate_number, user=user).first()

            if vehicle:
                roadfund_count = vehicle.road_funds.count()
                if roadfund_count > 0 :
                    return Response({'message': 'Road fund already registered for this plate'}, status=409)
                roadfund.vehicle_id = vehicle.id
                
            else:
                vehicle = Vehicle.objects.create(plate_number=plate_number, user=user)
                roadfund.vehicle_id = vehicle.id

            # update other docs
            bolo = Bolo.objects.filter(vehicle_id=current_vehicle_id).first()
            if bolo:
                bolo.vehicle_id = roadfund.vehicle_id
                bolo.save()
            fi = FullInsurance.objects.filter(vehicle_id=current_vehicle_id).first()
            if fi:
                fi.vehicle_id = roadfund.vehicle_id
                fi.save()
            tp = ThirdParty.objects.filter(vehicle_id=current_vehicle_id).first()
            if tp:
                tp.vehicle_id = roadfund.vehicle_id
                tp.save()


        if issue_date:
            roadfund.issue_date = issue_date
        if expire_date:
            roadfund.expire_date = expire_date
        roadfund.save()
        serializer = RoadFundSerializer(roadfund)

        return Response({'data':serializer.data}, status=200)
    
    #delete
    elif request.method == 'DELETE':
        if roadfund.image:
            roadfund.image.delete()
        roadfund.delete()
        return Response(status=204)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

        


            

            
            


                
    

