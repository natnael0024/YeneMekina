from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Advert
from .serializers import AdvertSerializer

@csrf_exempt
def advert_list(request):
    if request.method == 'GET':
        adverts = Advert.objects.all()
        serializer = AdvertSerializer(adverts, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = request.POST.copy()
        data['image'] = request.FILES.get('image')
        serializer = AdvertSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def advert_detail(request, pk):
    try:
        advert = Advert.objects.get(pk=pk)
    except Advert.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = AdvertSerializer(advert)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = request.POST.copy()
        data['image'] = request.FILES.get('image')
        serializer = AdvertSerializer(advert, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)
    elif request.method == 'DELETE':
        try:
            advert.delete()
            response_data = {'message': 'Advert deleted successfully'}
            return JsonResponse(response_data, status=201)
        except:
            response_data = {'error': 'Failed to delete advert'}
            return JsonResponse(response_data, status=402)
    return JsonResponse({'error': 'Invalid request method'}, status=405)