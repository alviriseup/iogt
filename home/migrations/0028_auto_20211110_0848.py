# Generated by Django 3.1.11 on 2021-11-10 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0027_auto_20211105_1237'),
    ]

    operations = [
        migrations.AlterField(
            model_name='manifestsettings',
            name='background_color',
            field=models.CharField(help_text='Background color member defines a placeholder background color for the application page to display before its stylesheet is loaded. (example: #FFF)', max_length=10, verbose_name='Background color'),
        ),
        migrations.AlterField(
            model_name='manifestsettings',
            name='description',
            field=models.CharField(help_text='Provide description for application', max_length=500, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='manifestsettings',
            name='display',
            field=models.CharField(choices=[('FULLSCREEN', 'fullscreen'), ('STANDALONE', 'standalone'), ('MINIMAL_UI', 'minimal-ui'), ('BROWSER', 'browser')], help_text="Determines the preferred display mode for the website. The possible values are: 'fullscreen', 'standalone', 'minimal-ui', 'browser'. A better choice would be to use standalone as it looks great on mobile as well. For further information refer to: https://developer.mozilla.org/en-US/docs/Web/Manifest/display#values", max_length=255, verbose_name='Browser UI'),
        ),
        migrations.AlterField(
            model_name='manifestsettings',
            name='name',
            field=models.CharField(help_text='Provide name that usually represents the name of the web application to user', max_length=255, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='manifestsettings',
            name='scope',
            field=models.CharField(help_text="Provide navigation scope to limit what web pages can be viewed Example: 'https://www.iogt.com/<page-url>/' limits navigation to <page-url> of https://www.iogt.com:", max_length=255, verbose_name='Scope'),
        ),
        migrations.AlterField(
            model_name='manifestsettings',
            name='short_name',
            field=models.CharField(help_text='Provide short name to be displayed, if there is not enough space to display full name', max_length=255, verbose_name='Short name'),
        ),
        migrations.AlterField(
            model_name='manifestsettings',
            name='start_url',
            field=models.CharField(help_text='Start URL is the preferred URL that should be loaded when the user launches the web application', max_length=255, verbose_name='Start URL'),
        ),
        migrations.AlterField(
            model_name='manifestsettings',
            name='theme_color',
            field=models.CharField(help_text='Theme color defines the default theme color for the application (example: #493174)', max_length=10, verbose_name='Theme color'),
        ),
    ]
