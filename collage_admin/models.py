from django.db import models

# Create your models here.


class Review(models.Model):
    author = models.CharField(max_length=100)
    image = models.ImageField(upload_to='reviews/')
    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta :
        db_table = 'review'
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'
        