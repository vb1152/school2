# Generated by Django 4.0.6 on 2022-10-18 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0037_alter_student_teacher'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='siblings_names',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
