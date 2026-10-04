from django.contrib import messages
from django.http import HttpResponseNotAllowed
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import ContactMessageForm
from .models import ContactMessage, FieldNote, SiteProfile, Story


def home(request, contact_form=None, tip_form=None):
    return render(
        request,
        "portfolio/home.html",
        {
            "stories": Story.objects.filter(is_published=True),
            "field_notes": FieldNote.objects.filter(is_published=True),
            "profile": SiteProfile.objects.get(pk=1),
            "contact_form": contact_form or ContactMessageForm(
                initial={"kind": ContactMessage.Kind.CONTACT}
            ),
            "tip_form": tip_form or ContactMessageForm(initial={"kind": ContactMessage.Kind.TIP}),
        },
    )


def contact(request):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])

    form = ContactMessageForm(request.POST)
    if form.is_valid():
        form.save()
        kind = form.cleaned_data["kind"]
        message = f"Your message has been sent. {SiteProfile.objects.get(pk=1).name} will be in touch."
        if kind == ContactMessage.Kind.TIP:
            message = "Your tip has been received. Thank you for sharing it."
        messages.success(request, message)
        return redirect(f"{reverse('home')}#contact")

    kind = form.data.get("kind")
    response = home(
        request,
        contact_form=form if kind == ContactMessage.Kind.CONTACT else None,
        tip_form=form if kind == ContactMessage.Kind.TIP else None,
    )
    response.status_code = 400
    return response


def story_detail(request, slug):
    story = get_object_or_404(Story.objects.filter(is_published=True), slug=slug)
    if not story.has_hosted_content and story.article_url:
        return redirect(story.article_url)
    return render(
        request,
        "portfolio/story_detail.html",
        {
            "story": story,
            "profile": SiteProfile.objects.get(pk=1),
        },
    )
