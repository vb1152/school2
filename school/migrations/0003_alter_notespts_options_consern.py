# Generated by Django 4.0.6 on 2022-07-27 09:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0002_alter_student_teacher_notespts'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='notespts',
            options={'ordering': ['date']},
        ),
        migrations.CreateModel(
            name='Consern',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='Date')),
                ('consern_type', models.CharField(max_length=200, verbose_name='Type of Concern')),
                ('strategy_used', models.CharField(max_length=300, verbose_name='Strategies Used')),
                ('num_weeks', models.PositiveSmallIntegerField(verbose_name='Number of weeks')),
                ('st_responce', models.CharField(max_length=300, verbose_name='Student Response')),
                ('teach_comm', models.CharField(max_length=300, verbose_name='Teacher Comments')),
                ('refers', models.CharField(choices=[('NO', 'No Referral'), ('R', 'Referral'), ('RES', 'Concern Resolved')], max_length=3)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stud_consern', to='school.student')),
                ('teacher', models.ForeignKey(limit_choices_to={'is_teacher': True}, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['date'],
            },
        ),
    ]
