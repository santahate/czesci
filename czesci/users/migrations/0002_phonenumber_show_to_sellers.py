# Generated by Django 5.2.3 on 2025-07-12 20:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='phonenumber',
            name='show_to_sellers',
            field=models.BooleanField(default=False),
        ),
    ]
