# Generated by Django 4.0.6 on 2022-08-14 16:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0028_readingscreening'),
    ]

    operations = [
        migrations.AddField(
            model_name='support',
            name='concern',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='concern_support', to='school.consern'),
        ),
    ]