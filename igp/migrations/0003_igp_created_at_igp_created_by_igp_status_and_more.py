# Generated by Django 5.1.5 on 2025-02-07 07:24

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("igp", "0002_alter_igpitem_igp"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="igp",
            name="created_at",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="igp",
            name="created_by",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="created_igps",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="igp",
            name="status",
            field=models.CharField(
                choices=[
                    ("pending", "Pending"),
                    ("confirm", "Confirm"),
                    ("processing", "Processing"),
                    ("delivered", "Delivered"),
                    ("cancelled", "Cancelled"),
                ],
                default="pending",
                max_length=10,
            ),
        ),
        migrations.AddField(
            model_name="igp",
            name="updated_at",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name="igp",
            name="updated_by",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="updated_igps",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
