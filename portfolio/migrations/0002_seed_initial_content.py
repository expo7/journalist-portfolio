from datetime import date

from django.db import migrations


def seed_initial_content(apps, schema_editor):
    Story = apps.get_model("portfolio", "Story")
    FieldNote = apps.get_model("portfolio", "FieldNote")

    Story.objects.bulk_create(
        [
            Story(
                title="The landlords buying a city one block at a time",
                slug="landlords-buying-a-city",
                publication="The City Ledger",
                published_on=date(2024, 6, 16),
                category="investigations",
                artwork="housing",
                deck="A yearlong examination of shell companies, eviction filings, and the families left searching for a home.",
                is_featured=True,
                sort_order=1,
            ),
            Story(
                title="At the edge of the flood map",
                slug="edge-of-the-flood-map",
                publication="Common Ground",
                published_on=date(2024, 4, 1),
                category="features",
                artwork="water",
                deck="For one river town, every storm brings a familiar question: stay, rebuild, or leave?",
                sort_order=2,
            ),
            Story(
                title="The quiet cuts inside public schools",
                slug="quiet-cuts-public-schools",
                publication="Statewatch",
                published_on=date(2024, 2, 1),
                category="investigations",
                artwork="school",
                deck="Thousands of pages of district budgets reveal where resources disappear before they reach classrooms.",
                sort_order=3,
            ),
        ]
    )
    FieldNote.objects.bulk_create(
        [
            FieldNote(
                title="What a public-records request can — and cannot — do",
                slug="public-records-request",
                published_on=date(2024, 5, 8),
                sort_order=1,
            ),
            FieldNote(
                title="On earning trust with sources who have every reason to be cautious",
                slug="earning-source-trust",
                published_on=date(2024, 3, 19),
                sort_order=2,
            ),
            FieldNote(
                title="The spreadsheet is not the story. It is the beginning.",
                slug="spreadsheet-is-the-beginning",
                published_on=date(2024, 1, 11),
                sort_order=3,
            ),
        ]
    )


def remove_initial_content(apps, schema_editor):
    apps.get_model("portfolio", "Story").objects.filter(
        slug__in=[
            "landlords-buying-a-city",
            "edge-of-the-flood-map",
            "quiet-cuts-public-schools",
        ]
    ).delete()
    apps.get_model("portfolio", "FieldNote").objects.filter(
        slug__in=[
            "public-records-request",
            "earning-source-trust",
            "spreadsheet-is-the-beginning",
        ]
    ).delete()


class Migration(migrations.Migration):
    dependencies = [("portfolio", "0001_initial")]

    operations = [migrations.RunPython(seed_initial_content, remove_initial_content)]
