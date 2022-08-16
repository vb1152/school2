# Generated by Django 4.0.6 on 2022-08-14 16:42

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0033_observation_concern'),
    ]

    operations = [
        migrations.AddField(
            model_name='observation',
            name='created_at',
            field=models.DateTimeField(db_index=True, default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='observation',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]