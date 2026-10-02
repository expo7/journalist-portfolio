from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import ContactMessage, FieldNote, SiteProfile, Story


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

    def test_home_displays_editable_profile_content(self):
        profile = SiteProfile.objects.get(pk=1)
        profile.name = "Updated Reporter"
        profile.save()

        response = self.client.get(reverse("home"))

        self.assertContains(response, "Updated Reporter")

    def test_story_detail_displays_hosted_article_and_publication_link(self):
        story = Story.objects.create(
            title="Hosted story",
            slug="hosted-story",
            publication="The Ledger",
            published_on=date(2024, 1, 1),
            category=Story.Category.INVESTIGATION,
            deck="A hosted story deck.",
            article_body="First paragraph.\n\nSecond paragraph.",
            article_url="https://example.com/original-story",
        )

        response = self.client.get(reverse("story_detail", args=(story.slug,)))

        self.assertContains(response, "First paragraph.")
        self.assertContains(response, "Read at The Ledger")
        self.assertContains(response, story.article_url)

    def test_story_detail_does_not_expose_unpublished_story(self):
        story = Story.objects.create(
            title="Draft story",
            slug="draft-story",
            publication="The Ledger",
            published_on=date(2024, 1, 1),
            category=Story.Category.INVESTIGATION,
            deck="A draft story deck.",
            is_published=False,
        )

        response = self.client.get(reverse("story_detail", args=(story.slug,)))

        self.assertEqual(response.status_code, 404)


class AdminTests(TestCase):
    def test_admin_exposes_story_management_to_staff(self):
        user = get_user_model().objects.create_user("editor", "editor@example.com")
        user.is_staff = True
        user.is_superuser = True
        user.save()
        self.client.force_login(user)

        response = self.client.get(reverse("admin:portfolio_story_changelist"))

        self.assertEqual(response.status_code, 200)

        add_response = self.client.get(reverse("admin:portfolio_story_add"))
        self.assertContains(add_response, 'name="article_body"')
        self.assertContains(add_response, 'name="article_file"')

    def test_admin_exposes_profile_photo_upload_and_message_inbox(self):
        user = get_user_model().objects.create_user("editor", "editor@example.com")
        user.is_staff = True
        user.is_superuser = True
        user.save()
        self.client.force_login(user)
        profile = SiteProfile.objects.get(pk=1)

        profile_response = self.client.get(
            reverse("admin:portfolio_siteprofile_change", args=(profile.pk,))
        )
        inbox_response = self.client.get(reverse("admin:portfolio_contactmessage_changelist"))

        self.assertContains(profile_response, 'name="headshot"')
        self.assertEqual(inbox_response.status_code, 200)


class ContactFormTests(TestCase):
    def test_contact_form_stores_a_message(self):
        response = self.client.post(
            reverse("contact"),
            {
                "kind": ContactMessage.Kind.CONTACT,
                "name": "Reader",
                "email": "reader@example.com",
                "message": "I would like to discuss a story idea.",
                "website": "",
            },
        )

        self.assertRedirects(response, f"{reverse('home')}#contact")
        message = ContactMessage.objects.get()
        self.assertEqual(message.name, "Reader")
        self.assertEqual(message.kind, ContactMessage.Kind.CONTACT)
        self.assertFalse(message.is_read)

    def test_anonymous_tip_can_be_submitted(self):
        response = self.client.post(
            reverse("contact"),
            {
                "kind": ContactMessage.Kind.TIP,
                "name": "",
                "email": "",
                "message": "Please investigate the contracts awarded last month.",
                "website": "",
            },
        )

        self.assertRedirects(response, f"{reverse('home')}#contact")
        message = ContactMessage.objects.get()
        self.assertEqual(message.kind, ContactMessage.Kind.TIP)
        self.assertEqual(message.name, "")

    def test_contact_form_rejects_honeypot_submissions(self):
        response = self.client.post(
            reverse("contact"),
            {
                "kind": ContactMessage.Kind.TIP,
                "message": "Spam message",
                "website": "https://spam.example",
            },
        )

        self.assertEqual(response.status_code, 400)
        self.assertFalse(ContactMessage.objects.exists())
