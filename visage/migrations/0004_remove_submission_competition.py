# Generated by Django 2.0.6 on 2018-07-04 00:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('visage', '0003_problem_competition'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='submission',
            name='competition',
        ),
    ]