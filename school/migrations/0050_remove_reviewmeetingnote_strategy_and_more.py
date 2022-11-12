# Generated by Django 4.0.6 on 2022-11-12 16:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0049_rename_reviewmeetingnotes_reviewmeetingnote'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reviewmeetingnote',
            name='strategy',
        ),
        migrations.AddField(
            model_name='reviewmeetingnote',
            name='strategy',
            field=models.ManyToManyField(related_name='strategy_name', to='school.implicitstrategy'),
        ),
    ]