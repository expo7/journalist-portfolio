import json
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from portfolio.models import FieldNote, SiteProfile, Story


class Command(BaseCommand):
    help = "Import a portable profile, story, and field-note fixture."

    def add_arguments(self, parser):
        parser.add_argument(
            "--fixture",
            type=Path,
            default=Path(settings.BASE_DIR) / "portfolio" / "fixtures" / "editorial_content.json",
            help="Path to an editorial content fixture.",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Validate the fixture without writing changes.",
        )

    def handle(self, *args, **options):
        fixture_path = options["fixture"]
        try:
            entries = json.loads(fixture_path.read_text(encoding="utf-8"))
        except OSError as error:
            raise CommandError(f"Unable to read fixture {fixture_path}: {error}") from error
        except json.JSONDecodeError as error:
            raise CommandError(f"Fixture {fixture_path} is not valid JSON: {error}") from error

        if not isinstance(entries, list):
            raise CommandError("Fixture root must be a list.")

        records = {
            "portfolio.siteprofile": [],
            "portfolio.story": [],
            "portfolio.fieldnote": [],
        }
        for entry in entries:
            if not isinstance(entry, dict) or entry.get("model") not in records:
                raise CommandError("Fixture may contain only site profiles, stories, and field notes.")
            if not isinstance(entry.get("fields"), dict):
                raise CommandError("Every fixture entry must have a fields object.")
            records[entry["model"]].append(entry["fields"].copy())

        if len(records["portfolio.siteprofile"]) != 1:
            raise CommandError("Fixture must contain exactly one site profile.")

        with transaction.atomic():
            SiteProfile.objects.update_or_create(pk=1, defaults=records["portfolio.siteprofile"][0])

            story_count = 0
            for fields in records["portfolio.story"]:
                slug = fields.pop("slug", None)
                if not slug:
                    raise CommandError("Every story must have a slug.")
                Story.objects.update_or_create(slug=slug, defaults=fields)
                story_count += 1

            note_count = 0
            for fields in records["portfolio.fieldnote"]:
                slug = fields.pop("slug", None)
                if not slug:
                    raise CommandError("Every field note must have a slug.")
                FieldNote.objects.update_or_create(slug=slug, defaults=fields)
                note_count += 1

            if options["dry_run"]:
                transaction.set_rollback(True)

        action = "Validated" if options["dry_run"] else "Imported"
        self.stdout.write(
            self.style.SUCCESS(f"{action} 1 site profile, {story_count} stories, and {note_count} field notes.")
        )
