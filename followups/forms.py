from django import forms
from .models import FollowUp


class FollowUpForm(forms.ModelForm):
    class Meta:
        model = FollowUp
        fields = ["patient_name", "phone", "language", "due_date", "notes"]
        widgets = {
            "due_date": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ensure the date field accepts the HTML5 date format
        self.fields["due_date"].input_formats = ["%Y-%m-%d"]

    def clean_phone(self):
        phone = self.cleaned_data["phone"]
        if not phone.isdigit() or len(phone) < 8:
            raise forms.ValidationError("Enter a valid phone number.")
        return phone