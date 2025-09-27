from django import forms

from accounts.models import CustomUser
from .models import Grade

class GradeForm(forms.ModelForm):
    student = forms.ModelChoiceField(
        queryset=CustomUser.objects.filter(role='user'),
        label="Студент",
        widget=forms.Select(attrs={"class": "border rounded p-2 w-full"})
    )

    class Meta:
        model = Grade
        fields = ["student", "subject", "grade", "date", "detail"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date", "class": "border rounded p-2 w-full"}),
            "student": forms.Select(attrs={"class": "border rounded p-2 w-full"}),
            "subject": forms.Select(attrs={"class": "border rounded p-2 w-full"}),
            "grade": forms.NumberInput(attrs={"class": "border rounded p-2 w-full"}),
            "detail": forms.Textarea(attrs={"class": "border rounded p-2 w-full", "rows": 3}),
        }

        labels = {
            "subject": "Предмет",
            "grade": "Оцінка",
            "date": "Дата",
            "detail": "Деталі",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['student'].label_from_instance = lambda obj: f"{obj.first_name} {obj.last_name}"