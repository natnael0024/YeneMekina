from rest_framework import serializers
from .models import Article
from .models import Map

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'
class MapSerializer(serializers.ModelSerializer):
    class Meta:
        model=Map
        fields='__all__'
