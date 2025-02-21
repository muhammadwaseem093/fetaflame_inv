# Generated by Django 5.1.5 on 2025-02-01 05:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("employees", "0003_remove_employee_previous_job_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="AttendanceSettings",
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
                ("work_start", models.TimeField(default="08:00:00")),
                ("work_end", models.TimeField(default="17:00:00")),
                ("break_start", models.TimeField(default="13:00:00")),
                ("break_end", models.TimeField(default="14:00:00")),
            ],
        ),
        migrations.CreateModel(
            name="Attendance",
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
                ("date", models.DateField(auto_now=True)),
                ("check_in", models.TimeField(blank=True, null=True)),
                ("check_out", models.TimeField(blank=True, null=True)),
                ("total_hours", models.FloatField(blank=True, null=True)),
                ("is_late", models.BooleanField(default=False)),
                ("is_early_leave", models.BooleanField(default=False)),
                (
                    "employee",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="employees.employee",
                    ),
                ),
            ],
        ),
    ]
