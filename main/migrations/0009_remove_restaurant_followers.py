# Generated by Django 5.1.2 on 2024-10-27 00:04

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0008_restaurant_followers_restaurant_random_products"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="restaurant",
            name="followers",
        ),
    ]
