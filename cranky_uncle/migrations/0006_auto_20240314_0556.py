# Generated by Django 3.2.23 on 2024-03-14 05:56

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('questionnaires', '0029_auto_20220512_1350'),
        ('wagtailredirects', '0006_redirect_increase_max_length'),
        ('wagtailforms', '0004_add_verbose_name_plural'),
        ('home', '0054_auto_20231207_1936'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('wagtailmenus', '0023_remove_use_specific'),
        ('wagtailcore', '0066_collection_management_permissions'),
        ('cranky_uncle', '0005_alter_crankyuncle_trigger_string'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='CrankyUncle',
            new_name='Interactive',
        ),
        migrations.RenameModel(
            old_name='CrankyUncleChannel',
            new_name='InteractiveChannel',
        ),
    ]
