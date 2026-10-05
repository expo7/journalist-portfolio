from django.core.management.base import BaseCommand
from portfolio.models import Story


class Command(BaseCommand):
    help = "Add the wild-horses article supplied by Brendan; date awaits publisher verification."

    def handle(self, *args, **options):
        story, created = Story.objects.get_or_create(
            slug='urgent-crisis-wild-horses',
            defaults={
                'title': 'An urgent crisis: Wild horses freely roaming the reservation',
                'publication': 'Navajo-Hopi Observer',
                'published_on': None,
                'category': 'features',
                'topic': 'animals',
                'deck': 'Kandace Baez’s reporting on wild horses freely roaming the reservation.',
                'article_url': 'https://www.nhonews.com/features/an-urgent-crisis-wild-horses-freely-roaming-the-reservation/article_826a5e37-2bce-43ad-ad9f-1b425d6a57af.html',
                'is_published': True,
                'sort_order': 5,
            },
        )
        self.stdout.write(self.style.SUCCESS('Wild-horses article ready.'))
