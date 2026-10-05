from datetime import date

from django.core.management.base import BaseCommand
from portfolio.models import Story


class Command(BaseCommand):
    help = "Add Kandace’s co-authored Frontiers for Young Minds publication."

    def handle(self, *args, **options):
        Story.objects.get_or_create(
            slug='nature-detectives-ethnopharmacology',
            defaults={
                'title': 'Nature Detectives: How Scientists Find New Medicines Through Ethnopharmacology',
                'publication': 'Frontiers for Young Minds',
                'published_on': date(2026, 4, 8),
                'category': 'features',
                'topic': 'nature',
                'deck': 'Co-authored by Kandace Baez: science writing for young readers on traditional knowledge, natural materials, and how scientists investigate potential medicines.',
                'article_url': 'https://kids.frontiersin.org/articles/10.3389/frym.2026.1689800',
                'is_published': True,
                'sort_order': 6,
            },
        )
        self.stdout.write(self.style.SUCCESS('Co-authored Nature Detectives article ready.'))
