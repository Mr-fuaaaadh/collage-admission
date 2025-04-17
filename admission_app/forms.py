from django import forms
from collages.models import Admission




class AdmissionApplicationForm(forms.ModelForm):
    class Meta:
        model = Admission
        fields = '__all__'
        widgets = {
            'course': forms.TextInput(attrs={
                'class': 'form-control rounded-pill',
                'placeholder': 'Course Name',
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control rounded-pill',
                'placeholder': 'Name',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control rounded-pill',
                'placeholder': 'Email',
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control rounded-pill',
                'placeholder': 'Phone',
            }),
            'state': forms.TextInput(attrs={
                'class': 'form-control rounded-pill',
                'placeholder': 'State',
            }),
            'pincode': forms.TextInput(attrs={
                'class': 'form-control rounded-pill',
                'placeholder': 'PIN',
            }),
            'qualification': forms.TextInput(attrs={
                'class': 'form-control rounded-pill',
                'placeholder': ' qualification',
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control rounded-4',
                'placeholder': 'Write your message or query here...',
                'rows': 3,
            }),
        }