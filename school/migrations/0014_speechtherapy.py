# Generated by Django 4.0.6 on 2022-08-04 13:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0013_rename_student_ot_ocupationaltherapy_stud_ot'),
    ]

    operations = [
        migrations.CreateModel(
            name='SpeechTherapy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('screen_date', models.DateField(verbose_name='Screen Speech Date')),
                ('add_notes', models.CharField(max_length=2000, verbose_name='Additional Notes')),
                ('scr_res', models.CharField(max_length=2000, verbose_name='Screening Results / Recommendations')),
                ('stud_st', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.student')),
                ('teacher', models.ForeignKey(limit_choices_to={'is_teacher': True}, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='teacher_st', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-screen_date'],
            },
        ),
    ]