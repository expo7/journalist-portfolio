from datetime import date
from django.core.management.base import BaseCommand
from portfolio.models import SiteProfile, Story


class Command(BaseCommand):
    help = "Import article metadata verified against Kandace's downloaded publisher PDFs."

    def handle(self, *args, **options):
        rows = [
            ('2026-05-12', 'The man and the Sky', '7348a235-38a3-4403-a6d2-c08516ffe8e2', 'Part 1 of 3'),
            ('2026-05-19', 'Whatever was at the door', '7fca57cf-9439-4168-a609-3a084cbe2642', 'Part 2 of 3'),
            ('2026-05-26', 'The Mountains Don’t Forget', '355a9047-2ae2-48b9-8906-131467bc490f', 'Part 3 of 3'),
            ('2026-07-28', 'Something Outside My Driver’s Window', '0bc8fc9f-d8e3-463a-a6ac-4a6681fa17b3', 'Episode 2 · Part 1 of 2'),
            ('2026-08-04', 'Something Outside My Driver’s Window — continued', 'e91bf84a-d0f9-4359-b28c-b6654ca7b425', 'Episode 2 · Continuation of the July 28 article'),
        ]
        for index, (day, subtitle, article_id, installment) in enumerate(rows):
            slug = 'theyre-here-mysteries-on-the-reservation' if index == 0 else 'theyre-here-' + day
            story, created = Story.objects.get_or_create(slug=slug, defaults={'title': 'They’re Here: ' + subtitle, 'publication': 'Navajo-Hopi Observer', 'published_on': date.fromisoformat(day), 'category': 'features', 'topic': 'mysteries', 'artwork': 'night', 'deck': installment + ' of Kandace Baez’s series, They’re Here: Mysteries on the Reservation.', 'article_url': 'https://www.nhonews.com/features/theyre-here-mysteries-on-the-reservation/article_' + article_id + '.html', 'is_featured': index == 0, 'sort_order': index})
            if index == 0 and not story.article_body and not story.article_file:
                story.title = 'They’re Here: ' + subtitle
                story.published_on = date.fromisoformat(day)
                story.article_url = 'https://www.nhonews.com/features/theyre-here-mysteries-on-the-reservation/article_' + article_id + '.html'
                story.deck = installment + ' of Kandace Baez’s series, They’re Here: Mysteries on the Reservation.'
                story.artwork = 'night'
                story.save()
        SiteProfile.objects.filter(pk=1).update(publication_credit='Special contributor to the Navajo-Hopi Observer')
        self.stdout.write(self.style.SUCCESS('Five article links prepared from publisher PDF metadata.'))
