from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Bolo
from .serializers import BoloSerializer
from vehicle.models import Vehicle
from django.views.decorators.csrf import csrf_exempt

# @login_required
def bolo_list_view(request):
    user_id = request.user.id
    # bolos = Bolo.objects.filter(vehicle__user_id=user_id).order_by('-created_at')
    bolos = Bolo.objects.order_by('-created_at')
    serializer = BoloSerializer(bolos, many=True)
    return JsonResponse(serializer.data, safe=False)

# @login_required
@csrf_exempt
def bolo_create_view(request):
    if request.method == 'POST':
        plate_number = request.POST.get('plate_number')
        inspection_date = request.POST.get('inspection_date')
        expire_date = request.POST.get('expire_date')
        image = request.FILES.get('image')

        # Validation
        # if not all([plate_number, inspection_date, expire_date]):
        #     return JsonResponse({'message': 'Missing required fields : plate_number, inspection_date, expire_date'}, status=400)

        # vehicle = Vehicle.objects.filter(user=request.user, plate_number=plate_number).first()

        # if vehicle:
        #     if vehicle.bolos.count() > 0:
        #         return JsonResponse({'message': 'Bolo already registered for this plate'}, status=409)

            # if vehicle.roadfunds.count() < 1:
            #     RoadFund.objects.create(vehicle=vehicle)

            # if vehicle.thirdparties.count() < 1:
            #     ThirdParty.objects.create(vehicle=vehicle)

            # if vehicle.fullinsurances.count() < 1:
            #     FullInsurance.objects.create(vehicle=vehicle)

            # if vehicle.oils.count() < 1:
            #     Oil.objects.create(vehicle=vehicle)

            # vehicle_id = vehicle.id
        # else:
        vehicle = Vehicle.objects.create(plate_number=plate_number)
            # RoadFund.objects.create(vehicle=vehicle)
            # ThirdParty.objects.create(vehicle=vehicle)
            # FullInsurance.objects.create(vehicle=vehicle)
            # Oil.objects.create(vehicle=vehicle)
        vehicle_id = vehicle.id

        bolo = Bolo.objects.create(
            vehicle_id=vehicle_id,
            inspection_date=inspection_date,
            expire_date=expire_date,
            image=image,
            notification_status=False
        )
        serializer = BoloSerializer(bolo)
        return JsonResponse(serializer.data, status=201)

# @login_required
@csrf_exempt
def bolo_detail_view(request, id):
    # bolo = get_object_or_404(Bolo, id=id, vehicle__user=request.user)
    bolo = get_object_or_404(Bolo, id=id)
    serializer = BoloSerializer(bolo)
    return JsonResponse(serializer.data)

# @login_required
@csrf_exempt
def bolo_update_view(request, id):
    bolo = get_object_or_404(Bolo, id=id, vehicle__user=request.user)

    if request.method == 'PUT':
        plate_number = request.POST.get('plate_number')
        inspection_date = request.POST.get('inspection_date')
        expire_date = request.POST.get('expire_date')
        image = request.FILES.get('image')

        if plate_number:
            current_vehicle_id = bolo.vehicle_id

            vehicle = Vehicle.objects.filter(user=request.user, plate_number=plate_number).first()

            if vehicle:
                bolo_exist = Bolo.objects.filter(vehicle_id=vehicle.id).exclude(id=id).exists()

                if bolo_exist:
                    return JsonResponse({'message': 'Bolo already exists for this plate'}, status=409)

                bolo.vehicle_id = vehicle.id
            else:
                vehicle = Vehicle.objects.create(user=request.user, plate_number=plate_number)
                bolo.vehicle_id = vehicle.id

            # rf = RoadFund.objects.filter(vehicle_id=current_vehicle_id).first()
            # if rf:
            #     rf.vehicle_id = bolo.vehicle_id
            #     rf.save()

            # fi = FullInsurance.objects.filter(vehicle_id=current_vehicle_id).first()
            # if fi:
            #     fi.vehicle_id = bolo.vehicle_id
            #     fi.save()

            # tp = ThirdParty.objects.filter(vehicle_id=current_vehicle_id).first()
            # if tp:
            #     tp.vehicle_id = bolo.vehicle_id
            #     tp.save()

            # oil = Oil.objects.filter(vehicle_id=current_vehicle_id).first()
            # if oil:
            #     oil.vehicle_id = bolo.vehicle_id
            #     oil.save()

        if image:
            if bolo.image:
                bolo.image.delete()
            bolo.image = image

        if inspection_date:
            bolo.inspection_date = inspection_date

        if expire_date:
            bolo.expire_date = expire_date

        bolo.save()
        serializer = BoloSerializer(bolo)
        return JsonResponse(serializer.data)

# @login_required
@csrf_exempt
def bolo_delete_view(request, id):
    # bolo = get_object_or_404(Bolo, id=id, vehicle__user=request.user)
    bolo = get_object_or_404(Bolo, id=id)
    if bolo.image:
        bolo.image.delete()
    bolo.delete()
    return JsonResponse({}, status=204)