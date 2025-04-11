from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from admission_app.models import University
from django.core.cache import cache

@receiver([post_save, post_delete], sender=University)
def clear_university_cache(sender, **kwargs):
    cache.delete('university_list')
