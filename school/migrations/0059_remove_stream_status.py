# Generated by Django 4.0.6 on 2022-11-14 20:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0058_remove_stream_stream_prev_stream_stream_next'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stream',
            name='status',
        ),
    ]
