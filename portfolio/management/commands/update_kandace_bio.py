from django.core.management.base import BaseCommand
from portfolio.models import SiteProfile


class Command(BaseCommand):
    help = "Update About and favorite quotes from the supplied August 2025 research-group introduction."

    def handle(self, *args, **options):
        profile = SiteProfile.objects.get(pk=1)
        profile.about_heading = 'Curiosity, compassion, and a search for answers.'
        profile.bio = 'I am Kandace Baez, an independent journalist based in Arizona. My reporting interests span animal rights, unexplained mysteries, and the natural world.\n\nI completed my master’s degree at Northern Arizona University in 2022 and joined the Ethnopharmacology & Zoopharmacognosy research group. My research has taken me to Uganda and Tanzania to investigate neuroactive and potentially psychoactive natural materials, including questions about whether wild chimpanzees and mountain gorillas intentionally use mind-altering plants, mushrooms, or insects.'
        profile.favorite_quote_one = 'If we can get people excited about animals, then by crikey, it makes it a heck of a lot easier to save them.'
        profile.favorite_quote_one_author = 'Steve Irwin'
        profile.favorite_quote_two = 'Every individual matters. Every individual has a role to play. Every individual makes a difference.'
        profile.favorite_quote_two_author = 'Dr. Jane Goodall'
        profile.save(update_fields=['about_heading', 'bio', 'favorite_quote_one', 'favorite_quote_one_author', 'favorite_quote_two', 'favorite_quote_two_author'])
        self.stdout.write(self.style.SUCCESS('Bio and favorite quotes updated.'))
