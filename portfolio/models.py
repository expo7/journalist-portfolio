from django.core.validators import FileExtensionValidator
from django.db import models


class Story(models.Model):
    class Category(models.TextChoices):
        INVESTIGATION = "investigations", "Investigation"
        FEATURE = "features", "Feature"

    class Artwork(models.TextChoices):
        HOUSING = "housing", "Housing"
        WATER = "water", "Water"
        SCHOOL = "school", "School"
        NIGHT = "night", "Night sky"

    title = models.CharField(max_length=180)
    slug = models.SlugField(unique=True)
    publication = models.CharField(max_length=80)
    published_on = models.DateField(blank=True, null=True)
    category = models.CharField(max_length=20, choices=Category.choices)
    artwork = models.CharField(max_length=20, choices=Artwork.choices, default=Artwork.HOUSING)
    topic = models.CharField(max_length=30, blank=True, choices=[("animals", "Animal rights"), ("mysteries", "UFOs & unexplained mysteries"), ("nature", "Wildlife & medicinal plants")])
    image = models.ImageField(upload_to="story-images/", blank=True)
    deck = models.TextField()
    article_body = models.TextField(
        blank=True,
        help_text="Optional full article text. Paragraph breaks are preserved on the public reading page.",
    )
    article_file = models.FileField(
        upload_to="articles/",
        blank=True,
        validators=[FileExtensionValidator(["pdf", "doc", "docx", "txt"])],
        help_text="Optional PDF, Word document, or plain-text version of the article.",
    )
    article_url = models.URLField(
        blank=True, help_text="Optional link to the published article at its original publication."
    )
    is_featured = models.BooleanField(default=False)
    is_published = models.BooleanField(default=True)
    sort_order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ("sort_order", "-published_on")

    def __str__(self):
        return self.title

    @property
    def reading_url(self):
        from django.urls import reverse
        return reverse('story_detail', args=[self.slug]) if self.has_hosted_content or not self.article_url else self.article_url

    @property
    def has_hosted_content(self):
        return bool(self.article_body or self.article_file)


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
    theme = models.CharField(
        max_length=20,
        choices=[("original", "Original — Paper Trail"), ("harbor", "Harbor Editorial — Navy & Ivory"), ("rose", "Harbor Rose — Plum & Ivory"), ("midnight", "Midnight — Deep Blue & White"), ("glow", "Midnight Glow — Soft Navy Gradient")],
        default="original",
        help_text="Choose the public website style. Save, then refresh the website to compare.",
    )
    show_field_notes = models.BooleanField(default=False)
    show_corkboard = models.BooleanField(default=True)
    show_support = models.BooleanField(default=True, help_text="Show reader support. Without a payment URL the button is a disabled preview.")
    support_url = models.URLField(blank=True, help_text="Paste her chosen hosted donation/payment page URL.")
    support_label = models.CharField(max_length=80, default="Buy me cat treats")
    favorite_quote_one = models.TextField(blank=True)
    favorite_quote_one_author = models.CharField(max_length=100, blank=True)
    favorite_quote_two = models.TextField(blank=True)
    favorite_quote_two_author = models.CharField(max_length=100, blank=True)
    pin_nav = models.BooleanField(default=False, help_text="Keep the navigation at the top while scrolling.")
    logo_style = models.CharField(max_length=20, choices=[("cat", "Cat — Curious Observer"), ("lighthouse", "Lighthouse — Clear Signal"), ("pen", "Pen & Star — Independent Voice")], default="cat")
    show_logo = models.BooleanField(default=True)
    logo = models.ImageField(upload_to="logos/", blank=True, help_text="Optional custom logo; otherwise the selected illustrated logo is used.")
    publication_credit = models.CharField(max_length=180, blank=True, default="Work published in the Navajo-Hopi Observer")
    publication_archive_url = models.URLField(blank=True)
    hero_art = models.CharField(max_length=20, choices=[("lighthouse", "Lighthouse"), ("corkboard", "Corkboard")], default="lighthouse")
    name = models.CharField(max_length=100, default="Kandace Baez")
    role = models.CharField(max_length=120, default="Independent investigative reporting")
    hero_headline = models.CharField(max_length=100, default="Follow the")
    hero_emphasis = models.CharField(max_length=100, default="paper trail.")
    intro = models.TextField(
        default="Kandace Baez reports on the systems that shape daily life: housing, public money, environmental risk, and the people pushing for answers."
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


class CorkboardItem(models.Model):
    title = models.CharField(max_length=180)
    summary = models.TextField(blank=True, help_text="Public-facing description only. Keep confidential research outside this board.")
    source_url = models.URLField(blank=True)
    status = models.CharField(max_length=20, choices=[("exploring", "Exploring"), ("requested", "Records requested"), ("reviewing", "Reviewing records"), ("published", "Published")], default="exploring")
    is_published = models.BooleanField(default=False)
    sort_order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ("sort_order", "pk")

    def __str__(self):
        return self.title
