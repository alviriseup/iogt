# Generated by Django 3.2.23 on 2024-02-29 05:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailforms', '0004_add_verbose_name_plural'),
        ('wagtailmenus', '0023_remove_use_specific'),
        ('questionnaires', '0029_auto_20220512_1350'),
        ('wagtailredirects', '0006_redirect_increase_max_length'),
        ('wagtailcore', '0066_collection_management_permissions'),
        ('home', '0056_auto_20240206_1239'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CrankyUncle',
        ),
    ]
