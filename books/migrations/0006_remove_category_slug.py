# Generated by Django 5.0.6 on 2024-07-01 21:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0005_alter_category_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='slug',
        ),
    ]
