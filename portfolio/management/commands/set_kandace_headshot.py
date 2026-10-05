from pathlib import Path
from django.conf import settings
from django.core.files import File
from django.core.management.base import BaseCommand
from portfolio.models import SiteProfile


class Command(BaseCommand):
    help = "Set the supplied portrait as Kandace’s editable profile photo."

    def handle(self, *args, **options):
        profile = SiteProfile.objects.get(pk=1)
        path = Path(settings.BASE_DIR) / 'portfolio/static/portfolio/kandace-profile.webp'
        with path.open('rb') as photo:
            profile.headshot.save('kandace-profile.webp', File(photo), save=True)
        self.stdout.write(self.style.SUCCESS('Profile photo updated.'))
