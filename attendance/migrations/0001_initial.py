# Generated by Django 5.1.7 on 2025-03-25 07:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("employees", "0007_alter_employee_face_encoding"),
    ]

    operations = [
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
                (
                    "attendance_type",
                    models.CharField(default="Check In", max_length=50),
                ),
                ("timestamp", models.DateTimeField(auto_now_add=True, null=True)),
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
