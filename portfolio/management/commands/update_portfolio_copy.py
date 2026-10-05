from django.core.management.base import BaseCommand
from portfolio.models import SiteProfile


class Command(BaseCommand):
    help = "Tailor portfolio introduction to Kandace’s published reporting and research."

    def handle(self, *args, **options):
        profile = SiteProfile.objects.get(pk=1)
        profile.hero_headline = 'A curious mind.'
        profile.hero_emphasis = 'A compassionate lens.'
        profile.role = 'Independent journalist & research collaborator'
        profile.intro = 'From wild horses on the reservation to unexplained sightings and the study of natural medicines, my work follows questions about animals, people, and the world we share.'
        profile.footer_tagline = 'Reporting and research guided by curiosity and compassion.'
        profile.save(update_fields=['hero_headline', 'hero_emphasis', 'role', 'intro', 'footer_tagline'])
        self.stdout.write(self.style.SUCCESS('Portfolio copy updated.'))
