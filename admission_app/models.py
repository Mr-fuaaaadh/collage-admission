from django.db import models
from django.utils.text import slugify
from django_ckeditor_5.fields import CKEditor5Field

class University(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True) 
    location = models.CharField(max_length=100)
    rank = models.CharField(max_length=100)
    image = models.ImageField(upload_to='university_images')
    description = models.TextField(null=True, blank=True)  # Optional field for additional information
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Automatically generate the slug based on the name
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    


class College(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True, null=True)  # Unique slug for SEO-friendly URLs
    location = models.CharField(max_length=255)
    established_year = models.PositiveIntegerField()
    accreditation = models.CharField(max_length=255, blank=True, null=True)  # Example: "NAAC A+", "UGC Approved"
    university_affiliated = models.CharField(max_length=255, blank=True, null=True)
    contact_email = models.EmailField(max_length=255, blank=True, null=True)
    contact_phone = models.CharField(max_length=20, blank=True, null=True)
    website = models.URLField(max_length=255, blank=True, null=True)
    content = CKEditor5Field(config_name='extends',blank=True, null=True)   # Detailed description of the college
    
    total_seats = models.PositiveIntegerField(default=0)
    available_seats = models.PositiveIntegerField(default=0)
    fee_structure = models.CharField(max_length=500, blank=True, null=True)
    
    image = models.ImageField(upload_to="college_images/", blank=True, null=True)  # Optional college image
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    




