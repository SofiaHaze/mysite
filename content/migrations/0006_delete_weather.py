# Generated by Django 4.0.6 on 2022-07-25 05:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0005_weather'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Weather',
        ),
    ]
