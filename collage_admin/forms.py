from django import forms
from admission_app.models import University 
from collages.models import Blog
from ckeditor.widgets import CKEditorWidget
from django.utils.text import slugify

class UniversityForm(forms.ModelForm):
    class Meta:
        model = University  
        fields = "__all__"



class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = "__all__"
        widgets = {
            'author': forms.TextInput(attrs={'class': 'form-control', 'id': 'id_author'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'id': 'id_title'}),
            'slug': forms.TextInput(attrs={'class': 'form-control', 'id': 'id_slug'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control', 'id': 'id_image'}),
            'content': CKEditorWidget(attrs={'class': 'form-control', 'id': 'id_content'}),  # CKEditor integration
        }
