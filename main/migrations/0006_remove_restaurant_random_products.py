# Generated by Django 5.1.2 on 2024-10-26 18:28

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0005_alter_food_id"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="restaurant",
            name="random_products",
        ),
    ]