# Generated by Django 5.1.5 on 2025-05-03 05:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Roomkhojlo_APP', '0021_alter_booking_contact_alter_booking_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='building',
            name='lattitude',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='building',
            name='longitude',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]
