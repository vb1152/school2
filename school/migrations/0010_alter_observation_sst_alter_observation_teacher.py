# Generated by Django 4.0.6 on 2022-07-31 08:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0009_observation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='observation',
            name='sst',
            field=models.ForeignKey(limit_choices_to={'is_sst': True}, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='sst_observation', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='observation',
            name='teacher',
            field=models.ForeignKey(limit_choices_to={'is_teacher': True}, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='observations_teacher', to=settings.AUTH_USER_MODEL),
        ),
    ]
