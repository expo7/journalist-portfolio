from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import FieldNote, Story


class HomeViewTests(TestCase):
    def test_home_only_shows_published_content(self):
        published_story = Story.objects.create(
            title="Published story",
            slug="published-story",
            publication="The Ledger",
            published_on=date(2024, 1, 1),
            category=Story.Category.INVESTIGATION,
            deck="A published story deck.",
            is_published=True,
        )
        Story.objects.create(
            title="Draft story",
            slug="draft-story",
            publication="The Ledger",
            published_on=date(2024, 1, 2),
            category=Story.Category.FEATURE,
            deck="A draft story deck.",
            is_published=False,
        )
        FieldNote.objects.create(
            title="Published note",
            slug="published-note",
            published_on=date(2024, 1, 3),
            is_published=True,
        )

        response = self.client.get(reverse("home"))

        self.assertContains(response, published_story.title)
        self.assertNotContains(response, "Draft story")
        self.assertContains(response, "Published note")


class AdminTests(TestCase):
    def test_admin_exposes_story_management_to_staff(self):
        user = get_user_model().objects.create_superuser("editor", "editor@example.com", "test-password")
        self.client.force_login(user)

        response = self.client.get(reverse("admin:portfolio_story_changelist"))

        self.assertEqual(response.status_code, 200)
