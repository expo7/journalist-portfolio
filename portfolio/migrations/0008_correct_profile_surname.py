from django.db import migrations

OLD_NAME = "Kandace Biaz"
NEW_NAME = "Kandace Baez"
OLD_INTRO = (
    "Kandace Biaz reports on the systems that shape daily life: housing, public money, "
    "environmental risk, and the people pushing for answers."
)
NEW_INTRO = (
    "Kandace Baez reports on the systems that shape daily life: housing, public money, "
    "environmental risk, and the people pushing for answers."
)


def correct_profile_name(apps, schema_editor):
    SiteProfile = apps.get_model("portfolio", "SiteProfile")
    profile = SiteProfile.objects.filter(pk=1).first()
    if profile is None:
        return
    changed = False
    if profile.name == OLD_NAME:
        profile.name = NEW_NAME
        changed = True
    if profile.intro == OLD_INTRO:
        profile.intro = NEW_INTRO
        changed = True
    if changed:
        profile.save(update_fields=["name", "intro"])


def restore_previous_name(apps, schema_editor):
    SiteProfile = apps.get_model("portfolio", "SiteProfile")
    profile = SiteProfile.objects.filter(pk=1).first()
    if profile is None:
        return
    changed = False
    if profile.name == NEW_NAME:
        profile.name = OLD_NAME
        changed = True
    if profile.intro == NEW_INTRO:
        profile.intro = OLD_INTRO
        changed = True
    if changed:
        profile.save(update_fields=["name", "intro"])


class Migration(migrations.Migration):
    dependencies = [("portfolio", "0007_alter_siteprofile_theme")]

    operations = [migrations.RunPython(correct_profile_name, restore_previous_name)]
