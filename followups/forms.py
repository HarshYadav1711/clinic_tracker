from django import forms
from .models import FollowUp


class FollowUpForm(forms.ModelForm):
    class Meta:
        model = FollowUp
        fields = ["patient_name", "phone", "language", "nationality", "due_date", "notes"]
        widgets = {
            "due_date": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ensure the date field uses HTML5 date format (YYYY-MM-DD)
        self.fields["due_date"].input_formats = ["%Y-%m-%d"]
        self.fields["due_date"].widget.format = "%Y-%m-%d"
        
        # If editing existing record, format the initial date value
        if self.instance and self.instance.pk and self.instance.due_date:
            self.initial["due_date"] = self.instance.due_date.strftime("%Y-%m-%d")

    def clean_phone(self):
        phone = self.cleaned_data["phone"]
        if not phone.isdigit() or len(phone) < 8:
            raise forms.ValidationError("Enter a valid phone number.")
        return phone