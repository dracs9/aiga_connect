from django import forms

from .models import TrainingApplication


class TrainingApplicationForm(forms.ModelForm):
    """Форма заявки на тренировку"""

    class Meta:
        model = TrainingApplication
        fields = ["message"]
        widgets = {
            "message": forms.Textarea(attrs={"rows": 4, "class": "form-control"}),
        }
