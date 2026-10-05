from django.core.management.base import BaseCommand
from portfolio.models import SiteProfile


class Command(BaseCommand):
    help = "Use Arizona rather than a city in Kandace’s public location."

    def handle(self, *args, **options):
        profile = SiteProfile.objects.get(pk=1)
        profile.location = 'Arizona'
        profile.bio = profile.bio.replace('Flagstaff, Arizona', 'Arizona').replace('Flagstaff, AZ', 'Arizona')
        profile.save(update_fields=['location', 'bio'])
        self.stdout.write(self.style.SUCCESS('Location updated to Arizona.'))
