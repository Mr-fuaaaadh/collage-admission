from django.db import models
from admission_app.models import *

# Create your models here.

class Courses(models.Model):
    """Model representing a college academic program (like BBA, BCom, MBA)."""

    LEVEL_CHOICES = [
        ('ug', 'Undergraduate'),
        ('pg', 'Postgraduate'),
        ('diploma', 'Diploma'),
        ('certificate', 'Certificate'),
    ]

    MODE_CHOICES = [
        ('full-time', 'Full Time'),
        ('part-time', 'Part Time'),
        ('distance', 'Distance Education'),
    ]

    name = models.CharField(max_length=100)
    college = models.ForeignKey(College, on_delete=models.CASCADE, related_name='college_courses')
    image = models.ImageField(upload_to='courses/', blank=True, null=True)
    description = CKEditor5Field(config_name='extends')
    duration_years = models.DecimalField(max_digits=3, decimal_places=1, help_text="Course duration in years (e.g., 3, 2.5)",default=0.0)
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default='ug')
    mode = models.CharField(max_length=20, choices=MODE_CHOICES, default='full-time')
    schedule = models.CharField(max_length=100, blank=True, help_text="E.g., June Intake, Academic Year 2025-26", default="")
    fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, help_text="Course fee in INR", null=True, blank=True)
    is_active = models.BooleanField(default=True, null=True, blank=True, help_text="Is the course currently active?")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Date when the course was created")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'College Course'
        verbose_name_plural = 'College Courses'

    def __str__(self):
        return f"{self.name} - {self.college.name}"
    


class Blog(models.Model):
    """Model representing a blog post related to colleges."""
    author = models.CharField(max_length=100, help_text="Author of the blog post")
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, help_text="Unique URL-friendly identifier for the blog post")
    content = CKEditor5Field(config_name='extends')
    image = models.ImageField(upload_to='blogs/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Blog Post'
        verbose_name_plural = 'Blog Posts'

    def __str__(self):
        return self.title