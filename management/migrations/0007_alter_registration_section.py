# Generated by Django 4.0.5 on 2022-06-13 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0006_registration_created_at_registration_updated_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registration',
            name='section',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
    ]
