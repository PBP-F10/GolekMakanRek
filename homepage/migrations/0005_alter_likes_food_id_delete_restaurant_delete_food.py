# Generated by Django 5.1.1 on 2024-10-23 05:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0004_alter_food_id_alter_restaurant_id'),
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='likes',
            name='food_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.food'),
        ),
        migrations.DeleteModel(
            name='Restaurant',
        ),
        migrations.DeleteModel(
            name='Food',
        ),
    ]
