from django.db import models
from django.contrib.auth.models import AbstractUser


class MyUser(AbstractUser):
    is_sst = models.BooleanField(verbose_name='SST status', default=False)
    is_teacher = models.BooleanField(verbose_name='Teacher status', default=False)
    is_conselor = models.BooleanField(verbose_name='Conselor status', default=False)

    def __str__(self) -> str:
        return self.username


class Student(models.Model):
    school_id = models.CharField(max_length=10, verbose_name='school_id')
    first_name = models.CharField(
                    max_length=100,
                    verbose_name='First Name')
    middle_name = models.CharField(
                    max_length=100, 
                    blank=True, null=True,
                    verbose_name='Middle Name')
    last_name = models.CharField(
                    max_length=100,
                    verbose_name='Last Name')
    preferred_name = models.CharField(
                    max_length=100, 
                    blank=True, null=True,
                    verbose_name='Preferred Name')
    date_of_birth = models.DateField(verbose_name='DOB')
    birth_order_in_class = models.PositiveSmallIntegerField(
                                verbose_name='Birth order in class'
                                )
    birth_order_in_family = models.PositiveSmallIntegerField(
                                verbose_name='Birth order in family'
                                )
    MALE = 'M'
    FEMALE = 'F'
    GENDER_CHOICES = [(MALE, 'Male'),(FEMALE, 'Female'),]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)

    cur_grade = models.PositiveSmallIntegerField(verbose_name='Current Grade')
    grad_year = models.CharField(verbose_name='Graduation Year', max_length=4)
    email = models.EmailField(blank=True, null=True)
    home_lang = models.CharField(
                        verbose_name='Home Language',
                        max_length=100)
    date_join = models.DateField(verbose_name='Date of joining')
    entrygrades = models.PositiveSmallIntegerField()
    teacher = models.ForeignKey(MyUser, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name_plural = "Students"

    def __str__(self) -> str:
        return self.first_name + ' ' + self.last_name
