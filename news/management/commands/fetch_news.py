from django.core.management.base import BaseCommand
from django.utils import timezone
from dateutil import parser as dateparser
import feedparser

from news.models import Source, Article

class Command(BaseCommand):
    help = "Fetch news from configured sources (RSS/API)"

    def handle(self, *args, **options):
        sources = Source.objects.filter(enabled=True)
        created_count = 0
        for s in sources:
            if s.kind == 'rss':
                feed = feedparser.parse(s.url)
                for e in getattr(feed, 'entries', []):
                    url = e.get('link')
                    title = (e.get('title') or '').strip()
                    if not url or not title:
                        continue
                    if Article.objects.filter(url=url).exists():
                        continue
                    published_at = None
                    for key in ('published', 'updated', 'created'):
                        if e.get(key):
                            try:
                                published_at = dateparser.parse(e.get(key))
                                break
                            except Exception:
                                pass
                    Article.objects.create(
                        source=s,
                        title=title[:300],
                        url=url,
                        summary=(e.get('summary') or e.get('description') or '')[:2000],
                        author=(e.get('author') or '')[:200],
                        published_at=published_at or timezone.now(),
                        tags="",
                    )
                    created_count += 1
            else:
                # Placeholder for API-based sources
                pass
        self.stdout.write(self.style.SUCCESS(f"Created {created_count} articles."))
