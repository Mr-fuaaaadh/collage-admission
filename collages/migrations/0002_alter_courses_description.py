# Generated by Django 5.1.7 on 2025-04-05 04:46

import django_ckeditor_5.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('collages', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courses',
            name='description',
            field=django_ckeditor_5.fields.CKEditor5Field(),
        ),
    ]
