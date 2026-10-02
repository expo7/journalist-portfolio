from django import forms

from .models import ContactMessage


class ContactMessageForm(forms.ModelForm):
    website = forms.CharField(required=False, widget=forms.HiddenInput)

    class Meta:
        model = ContactMessage
        fields = ("kind", "name", "email", "message")
        widgets = {
            "kind": forms.HiddenInput,
            "name": forms.TextInput(attrs={"autocomplete": "name"}),
            "email": forms.EmailInput(attrs={"autocomplete": "email"}),
            "message": forms.Textarea(attrs={"rows": 6}),
        }

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("website"):
            raise forms.ValidationError("Unable to submit this message.")
        if cleaned_data.get("kind") == ContactMessage.Kind.CONTACT:
            if not cleaned_data.get("name"):
                self.add_error("name", "Please provide your name.")
            if not cleaned_data.get("email"):
                self.add_error("email", "Please provide your email address.")
        return cleaned_data
