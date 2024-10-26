# Generated by Django 5.1.2 on 2024-10-26 21:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resto_preview', '0010_show_resto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='follow',
            name='restaurant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='resto_preview.show_resto'),
        ),
        migrations.AlterField(
            model_name='rating',
            name='restaurant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='resto_preview.show_resto'),
        ),
    ]
