from tabnanny import verbose
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import clear_script_prefix


class MyUser(AbstractUser):
    is_sst = models.BooleanField(verbose_name='SST role', default=False)
    is_teacher = models.BooleanField(verbose_name='Teacher role', default=False)
    is_conselor = models.BooleanField(verbose_name='Conselor role', default=False)

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
    teacher = models.ForeignKey(MyUser, 
                                on_delete=models.SET_NULL, 
                                null=True,
                                limit_choices_to={'is_teacher': True})

    class Meta:
        verbose_name_plural = "Students"

    def __str__(self) -> str:
        return self.first_name + ' ' + self.last_name


class NotesPTS(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField()
    note = models.CharField(max_length=2000)

    class Meta:
        ordering = ['date']
    
class Consern(models.Model):
    date = models.DateField(verbose_name='Date')
    consern_type = models.CharField(verbose_name='Type of Concern', max_length=2000)
    strategy_used = models.CharField(verbose_name='Strategies Used', max_length=2000)
    num_weeks = models.PositiveSmallIntegerField(verbose_name='Number of weeks')
    st_responce = models.CharField(verbose_name='Student Response', max_length=2000)
    teach_comm = models.CharField(verbose_name='Teacher Comments', max_length=2000)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='stud_consern')
    teacher = models.ForeignKey(MyUser, 
                                on_delete=models.PROTECT, 
                                null=True,
                                limit_choices_to={'is_teacher': True})
    NOREFERRAL = 'NO'
    REFERRAL = 'R'
    RESOLVED = 'RES'
    CONSERN_CHOICES = [(NOREFERRAL, 'No Referral'),(REFERRAL, 'Referral'), (RESOLVED, 'Concern Resolved')]
    refers = models.CharField(max_length=3, choices=CONSERN_CHOICES, verbose_name='Referral')

    class Meta:
        ordering = ['-date']

class Intake(models.Model):
    timeline = models.PositiveSmallIntegerField(verbose_name='ST with teacher')
    sst_reasoning = models.CharField(verbose_name='Why to SST?', max_length=2000)
    behavior_patterns = models.CharField(verbose_name='Primary behavior patterns', max_length=2000)
    
    CARE = 'C'
    GUIDANCE = 'G'
    SOCIAL = 'S'
    BEHAVE_CHOICES = [
                        (CARE, 'A health, development, or academic issue (Care/Therapeutic)?'),
                        (GUIDANCE, 'A student pushing the school’s behavioral boundaries (Guidance and  Discipline)?'),
                        (SOCIAL, 'A student having difficulty understanding how to integrate into the fabric of their class (Social Inclusion)?')
                    ]
    behavior_quality = models.CharField(max_length=1, choices=BEHAVE_CHOICES, verbose_name='Qualify this behavior')
    why_consern = models.CharField(verbose_name='Concern reasoning', max_length=2000)
    what_done = models.CharField(verbose_name='What done', max_length=2000)
    smal_done = models.CharField(verbose_name='What done small', max_length=2000)
    didnt_worked = models.CharField(verbose_name='Not worked', max_length=2000)
    worse = models.CharField(verbose_name='Worse', max_length=2000)
    response_level = models.CharField(verbose_name='Responce level', max_length=2000)
    other_info = models.CharField(verbose_name='Other info for SST', max_length=2000)
    estim_result = models.CharField(verbose_name='Estimate result', max_length=2000)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='stud_intake', default=None)
    teacher = models.ForeignKey(MyUser, 
                                on_delete=models.PROTECT, 
                                null=True,
                                limit_choices_to={'is_teacher': True})
    concern = models.OneToOneField(Consern, on_delete=models.CASCADE, 
                                    related_name='consern_intake', 
                                    default=None, null=True, blank=True)    


class Observation(models.Model):
    date = models.DateField(verbose_name='Date')
    teacher = models.OneToOneField(MyUser, 
                                on_delete=models.PROTECT, 
                                null=True,
                                limit_choices_to={'is_teacher': True},
                                related_name='observations_teacher')
    sst = models.OneToOneField(MyUser, 
                                on_delete=models.PROTECT, 
                                null=True,
                                limit_choices_to={'is_sst': True},
                                related_name='sst_observation')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='stud_observation')
    note = models.CharField(verbose_name='Observation note', max_length=2000)

    class Meta:
        ordering = ["-date"]

    def __str__(self) -> str:
        return 'Observation_note'

        