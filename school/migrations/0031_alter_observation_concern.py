# Generated by Django 4.0.6 on 2022-08-14 16:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0030_observation_concern'),
    ]

    operations = [
        migrations.AlterField(
            model_name='observation',
            name='concern',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='observation_consern', to='school.consern'),
        ),
    ]
