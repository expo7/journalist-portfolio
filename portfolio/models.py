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
