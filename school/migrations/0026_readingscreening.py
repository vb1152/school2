# Generated by Django 4.0.6 on 2022-08-13 20:46

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0025_delete_readingscreening'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReadingScreening',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('date', models.DateField(verbose_name='Screen date')),
                ('notes', models.CharField(blank=True, max_length=2000, null=True, verbose_name='Additional notes')),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
    ]
