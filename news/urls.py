from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ArticleViewSet, SourceViewSet

router = DefaultRouter()
router.register(r'articles', ArticleViewSet, basename='article')
router.register(r'sources', SourceViewSet, basename='source')

urlpatterns = [
    path('', include(router.urls)),
]
