from datetime import date

from django.core.management.base import BaseCommand
from portfolio.models import Story


class Command(BaseCommand):
    help = "Add Kandace’s co-authored thermal energy storage paper."

    def handle(self, *args, **options):
        Story.objects.get_or_create(
            slug='underwater-thermal-energy-storage',
            defaults={
                'title': 'Electric-driven underwater thermal energy storage: Commercial utilization of surplus fluctuating wind power for district heating',
                'publication': 'Journal of Infrastructure, Policy and Development',
                'published_on': date(2025, 12, 19),
                'category': 'features',
                'deck': 'Co-authored by Kandace Baez: research exploring a proposed underwater thermal storage system that converts surplus wind electricity into heat for district heating.',
                'article_url': 'https://doi.org/10.24294/jipd9013',
                'is_published': True,
                'sort_order': 7,
            },
        )
        self.stdout.write(self.style.SUCCESS('Co-authored thermal energy paper ready.'))
