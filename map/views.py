from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests
from rest_framework.parsers import JSONParser
from .models import Map, Article
from .serializers import ArticleSerializer, MapSerializer
from decouple import config

@csrf_exempt
def article_list(request):
    if request.method == 'GET':
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = ArticleSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def article_detail(request, pk):
    try:
        article = Article.objects.get(pk=pk)
    except Article.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = ArticleSerializer(article)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = ArticleSerializer(article, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        article.delete()
        return HttpResponse(status=204)

@csrf_exempt
def map_store(request):
    if request.method == 'GET':
        map_objects = Map.objects.all()
        serializer = MapSerializer(map_objects, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = MapSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            Add = serializer.data
            api_key = config('API_TOKEN')
            url = 'https://mapapi.gebeta.app/api/v1/route/addPlace'
            data = {
                **Add,  #for simplify 'name':add['name'],'lat':add['lat'],'lon':add['lon'],'type':add['type'],'cty':add['city'],'country':add['country'],'phone':add['phone'],'email':add['email']
                'apiKey': api_key
            }
            response = requests.post(url, json=data)
            if response.status_code == 200:
                # Success
                
                return JsonResponse({'message': 'Place added successfully.'}, status=200)
            else:
                # Error
                return JsonResponse({'error': 'Failed to add place.'}, status=500)

    # Handle GET requests or other methods
    return JsonResponse({'error': 'Method not allowed.'}, status=405)