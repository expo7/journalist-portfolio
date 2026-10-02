from django.db import migrations


def seed_site_profile(apps, schema_editor):
    SiteProfile = apps.get_model("portfolio", "SiteProfile")
    SiteProfile.objects.get_or_create(
        pk=1,
        defaults={
            "name": "Kandace Biaz",
            "role": "Independent investigative reporting",
            "hero_headline": "Follow the",
            "hero_emphasis": "paper trail.",
            "intro": "Kandace Biaz reports on the systems that shape daily life: housing, public money, environmental risk, and the people pushing for answers.",
            "about_heading": "Reporting with care, rigor, and a little persistence.",
            "bio": "I am an independent journalist based in the Midwest, where I report long-form investigations and narrative features. My work has prompted public hearings, policy changes, and, most importantly, conversations that otherwise might not have happened.\n\nI believe the best investigations make complicated systems legible — without losing sight of the people living inside them.",
            "location": "Chicago, IL",
            "beats": "Housing · Climate · Power",
            "contact_email": "hello@kandacebiaz.com",
            "tip_email": "tips@kandacebiaz.com",
            "footer_tagline": "Independent journalism for the public interest.",
        },
    )


class Migration(migrations.Migration):
    dependencies = [("portfolio", "0003_contactmessage_siteprofile")]

    operations = [migrations.RunPython(seed_site_profile, migrations.RunPython.noop)]
