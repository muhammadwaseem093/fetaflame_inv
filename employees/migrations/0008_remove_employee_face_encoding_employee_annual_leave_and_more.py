# Generated by Django 5.1.7 on 2025-04-21 04:45

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("employees", "0007_alter_employee_face_encoding"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="employee",
            name="face_encoding",
        ),
        migrations.AddField(
            model_name="employee",
            name="annual_leave",
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="employee",
            name="basic_salary",
            field=models.DecimalField(
                blank=True, decimal_places=2, max_digits=10, null=True
            ),
        ),
        migrations.AddField(
            model_name="employee",
            name="casual_leave",
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="employee",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name="employee",
            name="food_allowance",
            field=models.DecimalField(
                blank=True, decimal_places=2, max_digits=10, null=True
            ),
        ),
        migrations.AddField(
            model_name="employee",
            name="house_allowance",
            field=models.DecimalField(
                blank=True, decimal_places=2, max_digits=10, null=True
            ),
        ),
        migrations.AddField(
            model_name="employee",
            name="marriage_allowance",
            field=models.DecimalField(
                blank=True, decimal_places=2, max_digits=10, null=True
            ),
        ),
        migrations.AddField(
            model_name="employee",
            name="medical_allowance",
            field=models.DecimalField(
                blank=True, decimal_places=2, max_digits=10, null=True
            ),
        ),
        migrations.AddField(
            model_name="employee",
            name="medical_leave",
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="employee",
            name="sick_leave",
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="employee",
            name="stauts",
            field=models.CharField(
                choices=[
                    ("active", "Active"),
                    ("on_leave", "On Leave"),
                    ("retired", "Retired"),
                    ("terminated", "Terminated"),
                ],
                default="Active",
                max_length=20,
            ),
        ),
        migrations.AddField(
            model_name="employee",
            name="traveling_allowance",
            field=models.DecimalField(
                blank=True, decimal_places=2, max_digits=10, null=True
            ),
        ),
        migrations.AddField(
            model_name="employee",
            name="updated_at",
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
