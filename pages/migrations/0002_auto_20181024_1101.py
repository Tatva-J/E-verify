# Generated by Django 2.1.2 on 2018-10-24 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='database',
            name='headshot',
            field=models.ImageField(blank=True, upload_to='author_headshots'),
        ),
    ]
