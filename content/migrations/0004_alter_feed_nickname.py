# Generated by Django 4.0.6 on 2022-07-23 03:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0003_feed_nickname'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feed',
            name='nickname',
            field=models.TextField(default=''),
        ),
    ]
