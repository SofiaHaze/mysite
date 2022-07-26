# Generated by Django 4.0.6 on 2022-07-25 05:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0004_alter_feed_nickname'),
    ]

    operations = [
        migrations.CreateModel(
            name='Weather',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weather', models.TextField()),
                ('email', models.EmailField(default='', max_length=254)),
                ('content', models.TextField()),
            ],
        ),
    ]
