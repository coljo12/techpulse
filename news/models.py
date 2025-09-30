from django.db import models

class Source(models.Model):
    KIND_CHOICES = (
        ('rss', 'RSS'),
        ('api', 'API'),
    )
    name = models.CharField(max_length=120)
    kind = models.CharField(max_length=10, choices=KIND_CHOICES, default='rss')
    url = models.URLField(unique=True)
    enabled = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Article(models.Model):
    source = models.ForeignKey(Source, on_delete=models.PROTECT, related_name='articles')
    title = models.CharField(max_length=300)
    url = models.URLField(unique=True)
    summary = models.TextField(blank=True)
    author = models.CharField(max_length=200, blank=True)
    published_at = models.DateTimeField(null=True, blank=True)
    tags = models.CharField(max_length=300, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [models.Index(fields=['-published_at'])]
        ordering = ['-published_at', '-created_at']

    def __str__(self):
        return self.title
