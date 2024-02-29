# Generated by Django 3.2.23 on 2024-02-29 05:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cranky_uncle', '0004_auto_20240215_0558'),
    ]

    operations = [
        migrations.AlterField(
            model_name='crankyuncle',
            name='trigger_string',
            field=models.CharField(blank=True, help_text='Language short code will postfix after trigger string e.g string_en', max_length=255, null=True),
        ),
    ]