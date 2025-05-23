# Generated by Django 5.1.5 on 2025-01-25 06:23

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("categories", "0001_initial"),
        ("items", "0001_initial"),
        ("units", "0001_initial"),
        ("vendor", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="OGP",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("ogp_number", models.CharField(max_length=20, unique=True)),
                ("date", models.DateField(default=django.utils.timezone.now)),
                (
                    "vehicle_number",
                    models.CharField(blank=True, max_length=20, null=True),
                ),
                (
                    "vehicle_type",
                    models.CharField(blank=True, max_length=50, null=True),
                ),
                ("driver_name", models.CharField(blank=True, max_length=50, null=True)),
                (
                    "driver_contact",
                    models.CharField(blank=True, max_length=15, null=True),
                ),
                ("address", models.CharField(max_length=100)),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="categories.category",
                    ),
                ),
                (
                    "messer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="vendor.vendor"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="OGPItem",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("description", models.TextField()),
                ("quantity", models.DecimalField(decimal_places=2, max_digits=10)),
                (
                    "item",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="items.item"
                    ),
                ),
                (
                    "ogp",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="items",
                        to="ogp.ogp",
                    ),
                ),
                (
                    "unit",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="units.unit"
                    ),
                ),
            ],
        ),
    ]
