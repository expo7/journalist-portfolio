from django.shortcuts import render

from .models import FieldNote, Story


def home(request):
    return render(
        request,
        "portfolio/home.html",
        {
            "stories": Story.objects.filter(is_published=True),
            "field_notes": FieldNote.objects.filter(is_published=True),
        },
    )
