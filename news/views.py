from rest_framework import viewsets, filters
from .models import Article, Source
from .serializers import ArticleSerializer, SourceSerializer

class ArticleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Article.objects.select_related('source').all()
    serializer_class = ArticleSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'summary', 'tags', 'source__name']
    ordering_fields = ['published_at', 'created_at']
    ordering = ['-published_at']

class SourceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Source.objects.filter(enabled=True)
    serializer_class = SourceSerializer
