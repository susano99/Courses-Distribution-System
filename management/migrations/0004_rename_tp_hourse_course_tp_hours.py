# Generated by Django 4.0.5 on 2022-06-12 19:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0003_alter_course_course_hours'),
    ]

    operations = [
        migrations.RenameField(
            model_name='course',
            old_name='tp_hourse',
            new_name='tp_hours',
        ),
    ]
