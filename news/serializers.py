from rest_framework import serializers
from .models import Article, Source

class SourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source
        fields = ['id', 'name', 'kind', 'url']

class ArticleSerializer(serializers.ModelSerializer):
    source = SourceSerializer(read_only=True)
    class Meta:
        model = Article
        fields = ['id', 'title', 'url', 'summary', 'author', 'published_at', 'tags', 'source']
