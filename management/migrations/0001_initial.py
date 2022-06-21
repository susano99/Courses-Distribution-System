# Generated by Django 4.0.5 on 2022-06-11 21:15

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=128)),
                ('language', models.CharField(max_length=128)),
                ('name', models.CharField(max_length=128)),
                ('is_elective', models.BooleanField(default=False)),
                ('semester', models.CharField(max_length=128)),
                ('full_hours', models.IntegerField()),
                ('tp_hourse', models.IntegerField()),
                ('td_hours', models.IntegerField()),
                ('nbr_of_credits', models.IntegerField()),
                ('department', models.CharField(max_length=128)),
                ('description', models.CharField(blank=True, max_length=128, null=True)),
                ('major', models.CharField(max_length=128)),
                ('is_archived', models.BooleanField(default=False)),
            ],
        ),
    ]