from django.contrib import admin

from .models import ContactMessage, FieldNote, SiteProfile, Story


@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    list_display = ("title", "publication", "published_on", "category", "is_featured", "is_published")
    list_filter = ("category", "is_featured", "is_published")
    list_editable = ("is_featured", "is_published")
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ("title", "publication", "deck")
    ordering = ("sort_order", "-published_on")
    fieldsets = (
        ("Publication", {"fields": ("title", "slug", "publication", "published_on", "category", "deck")}),
        (
            "Hosted article",
            {
                "fields": ("article_body", "article_file"),
                "description": "Paste the article text, upload a document, or use both. Uploaded documents are linked from the public reading page.",
            },
        ),
        ("External publication", {"fields": ("article_url",)}),
        ("Presentation", {"fields": ("artwork", "is_featured", "is_published", "sort_order")}),
    )


@admin.register(FieldNote)
class FieldNoteAdmin(admin.ModelAdmin):
    list_display = ("title", "published_on", "is_published")
    list_filter = ("is_published",)
    list_editable = ("is_published",)
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ("title",)
    ordering = ("sort_order", "-published_on")


@admin.register(SiteProfile)
class SiteProfileAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Identity and hero", {"fields": ("name", "role", "hero_headline", "hero_emphasis", "intro")}),
        ("About", {"fields": ("about_heading", "bio", "location", "beats", "headshot")}),
        ("Contact", {"fields": ("contact_email", "tip_email", "footer_tagline")}),
    )

    def has_add_permission(self, request):
        return not SiteProfile.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("kind", "sender", "email", "created_at", "is_read")
    list_filter = ("kind", "is_read", "created_at")
    list_editable = ("is_read",)
    search_fields = ("name", "email", "message")
    readonly_fields = ("kind", "name", "email", "message", "created_at")

    @admin.display(description="Sender")
    def sender(self, obj):
        return obj.name or "Anonymous"

    def has_add_permission(self, request):
        return False
