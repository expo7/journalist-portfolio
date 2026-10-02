from django.contrib import admin

from .models import FieldNote, Story


@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    list_display = ("title", "publication", "published_on", "category", "is_featured", "is_published")
    list_filter = ("category", "is_featured", "is_published")
    list_editable = ("is_featured", "is_published")
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ("title", "publication", "deck")
    ordering = ("sort_order", "-published_on")


@admin.register(FieldNote)
class FieldNoteAdmin(admin.ModelAdmin):
    list_display = ("title", "published_on", "is_published")
    list_filter = ("is_published",)
    list_editable = ("is_published",)
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ("title",)
    ordering = ("sort_order", "-published_on")
