# Generated by Django 5.0.3 on 2024-05-28 10:07

import django.db.models.deletion
import poultrypalace.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('poultrypalace', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='farmer',
            field=models.ForeignKey(default=poultrypalace.models.get_default_farmer_id, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
