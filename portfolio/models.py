from django.db import models


class Story(models.Model):
    class Category(models.TextChoices):
        INVESTIGATION = "investigations", "Investigation"
        FEATURE = "features", "Feature"

    class Artwork(models.TextChoices):
        HOUSING = "housing", "Housing"
        WATER = "water", "Water"
        SCHOOL = "school", "School"

    title = models.CharField(max_length=180)
    slug = models.SlugField(unique=True)
    publication = models.CharField(max_length=80)
    published_on = models.DateField()
    category = models.CharField(max_length=20, choices=Category.choices)
    artwork = models.CharField(max_length=20, choices=Artwork.choices, default=Artwork.HOUSING)
    deck = models.TextField()
    article_url = models.URLField(blank=True, help_text="Optional link to the published article.")
    is_featured = models.BooleanField(default=False)
    is_published = models.BooleanField(default=True)
    sort_order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ("sort_order", "-published_on")

    def __str__(self):
        return self.title


class FieldNote(models.Model):
    title = models.CharField(max_length=180)
    slug = models.SlugField(unique=True)
    published_on = models.DateField()
    article_url = models.URLField(blank=True, help_text="Optional link to the full note.")
    is_published = models.BooleanField(default=True)
    sort_order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ("sort_order", "-published_on")

    def __str__(self):
        return self.title


class SiteProfile(models.Model):
    name = models.CharField(max_length=100, default="Kandace Biaz")
    role = models.CharField(max_length=120, default="Independent investigative reporting")
    hero_headline = models.CharField(max_length=100, default="Follow the")
    hero_emphasis = models.CharField(max_length=100, default="paper trail.")
    intro = models.TextField(
        default="Kandace Biaz reports on the systems that shape daily life: housing, public money, environmental risk, and the people pushing for answers."
    )
    about_heading = models.CharField(
        max_length=160, default="Reporting with care, rigor, and a little persistence."
    )
    bio = models.TextField(
        default="I am an independent journalist based in the Midwest, where I report long-form investigations and narrative features. My work has prompted public hearings, policy changes, and, most importantly, conversations that otherwise might not have happened.\n\nI believe the best investigations make complicated systems legible — without losing sight of the people living inside them."
    )
    location = models.CharField(max_length=100, default="Chicago, IL")
    beats = models.CharField(max_length=180, default="Housing · Climate · Power")
    contact_email = models.EmailField(default="hello@kandacebiaz.com")
    tip_email = models.EmailField(default="tips@kandacebiaz.com")
    footer_tagline = models.CharField(max_length=180, default="Independent journalism for the public interest.")
    headshot = models.ImageField(upload_to="headshots/", blank=True)

    class Meta:
        verbose_name = "site profile"
        verbose_name_plural = "site profile"

    def __str__(self):
        return self.name


class ContactMessage(models.Model):
    class Kind(models.TextChoices):
        CONTACT = "contact", "Contact"
        TIP = "tip", "Confidential tip"

    kind = models.CharField(max_length=12, choices=Kind.choices)
    name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True)
    message = models.TextField(max_length=5000)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("is_read", "-created_at")

    def __str__(self):
        sender = self.name or self.email or "Anonymous"
        return f"{self.get_kind_display()} from {sender}"
