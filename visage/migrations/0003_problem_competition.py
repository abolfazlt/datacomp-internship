# Generated by Django 2.0.6 on 2018-07-03 15:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('visage', '0002_submission_competition'),
    ]

    operations = [
        migrations.AddField(
            model_name='problem',
            name='competition',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='visage.Competition', verbose_name='competition'),
        ),
    ]
