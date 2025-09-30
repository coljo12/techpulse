from django.contrib import admin
from .models import Source, Article

@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'kind', 'enabled', 'url')
    list_filter = ('kind', 'enabled')
    search_fields = ('name', 'url')

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'source', 'published_at', 'created_at')
    list_filter = ('source',)
    search_fields = ('title', 'summary', 'url')
