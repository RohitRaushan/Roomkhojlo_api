# Generated by Django 5.1.5 on 2025-04-25 16:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Roomkhojlo_APP', '0008_alter_employee_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='role',
            field=models.CharField(default='employee', max_length=50),
        ),
    ]
