from django.core.management.base import BaseCommand
from portfolio.models import SiteProfile, Story

ARTICLE_URL = "https://www.nhonews.com/features/theyre-here-mysteries-on-the-reservation/article_e91bf84a-d0f9-4359-b28c-b6654ca7b425.html"
ARCHIVE_URL = "https://www.nhonews.com/search/?l=25&s=start_time&sd=desc&f=html&t=article%2Cvideo%2Cyoutube%2Ccollection&app=editorial&nsa=eedition&q=kandace+baez"


class Command(BaseCommand):
    help = "Prepare the revised demo using Brendan's supplied article and editorial direction."

    def handle(self, *args, **options):
        profile = SiteProfile.objects.get(pk=1)
        profile.theme = "midnight"
        profile.location = "Flagstaff, AZ"
        profile.beats = "Animal rights · UFOs & mysteries · Wildlife & medicinal plants"
        profile.intro = "Independent reporting on animal rights, unexplained mysteries, and the natural world."
        profile.bio = "I am Kandace Baez, an independent journalist based in Flagstaff, Arizona. My interests include animal rights, UFOs and unexplained mysteries, and wildlife and medicinal plants."
        profile.publication_archive_url = ARCHIVE_URL
        profile.publication_credit = "Work published in the Navajo-Hopi Observer"
        profile.show_field_notes = False
        profile.save(update_fields=["theme", "location", "beats", "intro", "bio", "publication_archive_url", "publication_credit", "show_field_notes"])
        # Retain the original design examples as drafts; do not touch edited stories.
        examples = [("landlords-buying-a-city", "The landlords buying a city one block at a time", "The City Ledger"), ("edge-of-the-flood-map", "At the edge of the flood map", "Common Ground"), ("quiet-cuts-public-schools", "The quiet cuts inside public schools", "Statewatch")]
        for slug, title, publication in examples:
            Story.objects.filter(slug=slug, title=title, publication=publication, article_body="", article_url="", article_file="").update(is_published=False)
        Story.objects.get_or_create(slug="theyre-here-mysteries-on-the-reservation", defaults={"title": "They’re here: Mysteries on the reservation", "publication": "Navajo-Hopi Observer", "published_on": None, "category": "features", "topic": "mysteries", "artwork": "night", "deck": "Read Kandace’s published feature at the Navajo-Hopi Observer.", "article_url": ARTICLE_URL, "is_featured": True})
        self.stdout.write(self.style.SUCCESS("Demo prepared. Article date and full archive await verification; existing uploads and optional support settings retained."))
