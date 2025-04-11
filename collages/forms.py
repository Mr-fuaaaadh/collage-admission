from django import forms
from .models import Courses, College
from django_ckeditor_5.widgets import CKEditor5Widget

class CourseForm(forms.ModelForm):
    class Meta:
        model = Courses
        fields = "__all__"
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Course Name'}),
            'description': CKEditor5Widget(config_name='extends'),  # 👈 use CKEditor5Widget
            'duration_years': forms.NumberInput(attrs={'class': 'form-control'}),
            'fee': forms.NumberInput(attrs={'class': 'form-control'}),
            'college': forms.Select(attrs={'class': 'form-control'}),
            'level': forms.Select(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'mode': forms.Select(attrs={'class': 'form-control'}),
            'schedule': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Schedule'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),


        }

class CollageForm(forms.ModelForm):
    class Meta:
        model = College
        fields = "__all__"
        widgets = {
            'content': CKEditor5Widget(config_name='extends'),  # Rich text field
        }

    def __init__(self, *args, **kwargs):
        super(CollageForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name != 'content':
                field.widget.attrs.update({
                    'class': 'form-control',
                    'required': 'required',
                })
