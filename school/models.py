from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.urls import reverse


class MyUser(AbstractUser):
    is_sst = models.BooleanField(verbose_name='SST role', default=False)
    is_teacher = models.BooleanField(
        verbose_name='Teacher role', default=False)
    is_conselor = models.BooleanField(
        verbose_name='Counselor role', default=False)

    def __str__(self) -> str:
        return self.first_name + ' ' + self.last_name


class UsersData(models.Model):
    '''Model to store data from excel file. Person id, '''
    user = models.OneToOneField(
        MyUser, on_delete=models.CASCADE, related_name='users_data')
    person_id = models.CharField(max_length=10, verbose_name='personid')
    grades = models.CharField(max_length=100, verbose_name='grades')

    class Meta:
        verbose_name = 'Users data'

    def __str__(self) -> str:
        return self.user.username


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
    GENDER_CHOICES = [(MALE, 'Male'), (FEMALE, 'Female'), ]
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
                                limit_choices_to={'is_teacher': True},
                                related_name='students')
    siblings_names = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Students"

    def __str__(self) -> str:
        return self.first_name + ' ' + self.last_name

    @property
    def calculate_age(self):
        '''Calculate students age form date of birth'''
        from datetime import datetime
        from dateutil import relativedelta

        now = datetime.now()
        # convert string to date object
        start_date = datetime.strptime(str(self.date_of_birth), "%Y-%m-%d")
        # Get the relativedelta between two dates
        delta = relativedelta.relativedelta(now, start_date)
        return (delta.years, delta.months)


class NotesPTS(models.Model):
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name='student_notes')
    date = models.DateField()
    note = models.CharField(max_length=2000)

    class Meta:
        ordering = ['date']

    def __str__(self) -> str:
        return str(self.date)


# class Consern(models.Model):
#     date = models.DateField(verbose_name='Date')
#     # ACADEMIC = 'A'
#     # GUIDANCE = 'G'
#     # SOCIAL = 'S'
#     # CARE = 'C'
#     # TYPES_CHOICES = [(ACADEMIC, 'Academic'),
#     #                  (GUIDANCE, 'Guidance and Discipline'),
#     #                  (SOCIAL, 'Social Inclusion'),
#     #                  (CARE, 'Care and Therapeutic')]
#     # consern_type = models.CharField(
#     #     max_length=1, choices=TYPES_CHOICES, verbose_name='Type of Concern')
#     strategy_used = models.CharField(
#         verbose_name='Strategies Used', max_length=2000)
#     num_weeks = models.PositiveSmallIntegerField(
#         verbose_name='Number of weeks')
#     st_responce = models.CharField(
#         verbose_name='Student Response', max_length=2000)
#     teach_comm = models.CharField(
#         verbose_name='Teacher Comments', max_length=2000)
#     student = models.ForeignKey(
#         Student, on_delete=models.CASCADE, related_name='stud_consern')
#     teacher = models.ForeignKey(MyUser,
#                                 on_delete=models.PROTECT,
#                                 null=True,
#                                 limit_choices_to={'is_teacher': True})
#     NOREFERRAL = 'NO'
#     REFERRAL = 'R'
#     RESOLVED = 'RES'
#     CONSERN_CHOICES = [(NOREFERRAL, 'No Referral'),
#                        (REFERRAL, 'Referral'), (RESOLVED, 'Concern Resolved')]
#     refers = models.CharField(
#         max_length=3, choices=CONSERN_CHOICES, verbose_name='Referral')

#     class Meta:
#         ordering = ['-date']


class Intake(models.Model):
    timeline = models.PositiveSmallIntegerField(verbose_name='ST with teacher')
    sst_reasoning = models.CharField(
        verbose_name='Why to SST?', max_length=2000)
    behavior_patterns = models.CharField(
        verbose_name='Primary behavior patterns', max_length=2000)

    CARE = 'C'
    GUIDANCE = 'G'
    SOCIAL = 'S'
    BEHAVE_CHOICES = [
        (CARE, 'A health, development, or academic issue (Care/Therapeutic)?'),
        (GUIDANCE, 'A student pushing the school’s behavioral boundaries (Guidance and  Discipline)?'),
        (SOCIAL, 'A student having difficulty understanding how to integrate into the fabric of their class (Social Inclusion)?')
    ]
    behavior_quality = models.CharField(
        max_length=1, choices=BEHAVE_CHOICES, verbose_name='Qualify this behavior')

    why_consern = models.CharField(
        verbose_name='Concern reasoning', max_length=2000)
    what_done = models.CharField(verbose_name='What done', max_length=2000)
    smal_done = models.CharField(
        verbose_name='What done small', max_length=2000)
    didnt_worked = models.CharField(verbose_name='Not worked', max_length=2000)
    worse = models.CharField(verbose_name='Worse', max_length=2000)
    response_level = models.CharField(
        verbose_name='Responce level', max_length=2000)
    other_info = models.CharField(
        verbose_name='Other info for SST', max_length=2000)
    estim_result = models.CharField(
        verbose_name='Estimate result', max_length=2000)
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name='stud_intake', default=None)
    teacher = models.ForeignKey(MyUser,
                                on_delete=models.PROTECT,
                                null=True,
                                limit_choices_to={'is_teacher': True})

class BaseModel(models.Model):
    created_at = models.DateTimeField(db_index=True, default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Support(models.Model):
    date = models.DateField(verbose_name='Date')
    teacher = models.ForeignKey(MyUser,
                                on_delete=models.PROTECT,
                                null=True,
                                limit_choices_to={'is_teacher': True},
                                related_name='support_teacher')
    sst = models.ForeignKey(MyUser,
                            on_delete=models.PROTECT,
                            null=True,
                            limit_choices_to={'is_sst': True},
                            related_name='sst_support')
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name='stud_support')
    suport_text = models.CharField(
        verbose_name='Support text', max_length=2000)
    note = models.CharField(verbose_name='Support note', max_length=2000)
    # concern = models.ForeignKey(
    #     Consern, on_delete=models.CASCADE, related_name='concern_support', default=None)

    class Meta:
        ordering = ["-date"]

    def __str__(self) -> str:
        return self.suport_text[:15]


class OcupationalTherapy(BaseModel):
    screen_date = models.DateField(verbose_name='Screening Date')
    screen_time = models.TimeField(verbose_name='Screening Time')
    full_screen_recom = models.CharField(
        max_length=2000, verbose_name='Full Screening Recommended?')
    notes = models.CharField(max_length=2000, verbose_name='Notes')
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name='stud_ot', default=None)
    teacher = models.ForeignKey(MyUser,
                                on_delete=models.PROTECT,
                                null=True,
                                limit_choices_to={'is_teacher': True},
                                related_name='teacher_ot')

    class Meta:
        ordering = ['-screen_date']


class SpeechTherapy(BaseModel):
    screen_date = models.DateField(
        verbose_name='Screen Speech Date', help_text='Screen Speech Date')
    add_notes = models.CharField(
        max_length=2000, verbose_name='Additional Notes', help_text='Additional notes')
    scr_res = models.CharField(max_length=2000,
                               verbose_name='Screening Results / Recommendations',
                               help_text='Screening Results / Recommendations')
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name='stud_st', default=None)
    teacher = models.ForeignKey(MyUser,
                                on_delete=models.PROTECT,
                                null=True,
                                limit_choices_to={'is_teacher': True},
                                related_name='teacher_st')

    class Meta:
        ordering = ['-screen_date']

    def get_absolute_url(self):
        """Returns the URL to access a particular instance of MyModelName."""
        return reverse('school:show_speech_sst', kwargs={'pk': self.pk})

    def __str__(self) -> str:
        return str(self.screen_date)


class ResponceToSupport(BaseModel):
    support = models.ForeignKey(
        Support, on_delete=models.CASCADE, related_name='responce_support')
    date = models.DateField(verbose_name='Responce date')
    intervention = models.CharField(max_length=2000)
    note = models.CharField(max_length=2000)

    class Meta:
        ordering = ['-date']

    def __str__(self) -> str:
        return self.intervention[:15]


class ReadingScreening(BaseModel):
    INDEPENDENT = 'IND'
    INSTRUCTIONAL = 'IST'
    FRUSTRATIONAL = 'FRS'
    PP_FRUSTRATIONAL = 'PPF'
    READING_CHOISES = [(INDEPENDENT, 'Independent'),
                       (INSTRUCTIONAL, 'Instructional'),
                       (FRUSTRATIONAL, 'Frustrational'),
                       (PP_FRUSTRATIONAL, 'PP-Frustrational')]
    screen_type = models.CharField(
        max_length=3, choices=READING_CHOISES, verbose_name='Screening type')
    date_screen = models.DateField(verbose_name='Screen date')
    errors_screen = models.CharField(
        max_length=2000, verbose_name='Decoding errors')
    question_screen = models.CharField(
        max_length=2000, verbose_name='Comprehension questions')
    notes = models.CharField(max_length=2000, blank=True,
                             null=True, verbose_name='Additional notes')
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name='student_reading')
    teacher = models.ForeignKey(MyUser,
                                on_delete=models.PROTECT,
                                null=True,
                                limit_choices_to={'is_teacher': True},
                                related_name='teacher_read_screen')

    class Meta:
        ordering = ['-date_screen']

    def __str__(self) -> str:
        return self.screen_type[:15]


class Stream(BaseModel):
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name='stream_student')
    teacher = models.ForeignKey(MyUser,
                                on_delete=models.PROTECT,
                                null=True,
                                limit_choices_to={'is_teacher': True})
    date_start = models.DateField(verbose_name='Start date')
    date_review = models.DateField(verbose_name='Review Date')
    intake = models.OneToOneField(
        Intake, on_delete=models.CASCADE, related_name='stream_intake',
        blank=True, null=True)

    ONE = '1'
    TWO = '2'
    THREE = '3'
    FOUR = '4'
    FIVE = '5'
    SIX = '6'
    LEVEL_CHOICES = [
        (ONE, '1'),
        (TWO, '2'),
        (THREE, '3'),
        (FOUR, '4'),
        (FIVE, '5'),
        (SIX, '6'),
    ]
    level = models.CharField(
        max_length=1, choices=LEVEL_CHOICES, default=ONE, verbose_name='Stream level')

    CLOSED = 'CL'
    PROCEEDING = 'PR'
    OPEN = 'OP'
    STATUS_CHOICES = [
        (CLOSED, 'Closed'),
        (PROCEEDING, 'Proceeding'),
        (OPEN, 'Open'),
    ]
    status = models.CharField(
        max_length=2, choices=STATUS_CHOICES, default=OPEN, verbose_name='Status')
    support = models.ForeignKey(Support, on_delete=models.CASCADE,
                                null=True, related_name='stream_supports', verbose_name='Support')
    name = models.CharField(
        max_length=100, verbose_name='Stream name', default=None)
    stream_prev = models.ForeignKey(
        'self', on_delete=models.CASCADE, blank=True, null=True, 
        verbose_name='Previous Stream', related_name='prev_stream')

    YES = 'Y'
    NO = 'N'
    PROGRESS_CHOICES = [
        (YES, 'Yes'),
        (NO, 'No')
    ]
    progress = models.CharField(
        max_length=1, choices=PROGRESS_CHOICES, default=NO, verbose_name='Progress')

    class Meta:
        ordering = ["id"]

    def __str__(self) -> str:
        return self.name

class Observation(BaseModel):
    date = models.DateField(verbose_name='Date')
    teacher = models.ForeignKey(MyUser,
                                on_delete=models.PROTECT,
                                null=True,
                                limit_choices_to={'is_teacher': True},
                                related_name='observations_teacher')
    sst = models.ForeignKey(MyUser,
                            on_delete=models.PROTECT,
                            null=True,
                            limit_choices_to={'is_sst': True},
                            related_name='sst_observation')
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name='stud_observation')
    note = models.CharField(verbose_name='Observation note', max_length=2000)
    stream = models.ForeignKey(Stream, on_delete=models.PROTECT, related_name='sream_observation', default=None)

    class Meta:
        ordering = ["-date"]

    def __str__(self) -> str:
        return self.note[:50]

class ImplicitStrategy(BaseModel):
    '''Save names of the strategies for using in Review meetin notes'''
    name = models.CharField(
        max_length=2000, verbose_name='Implicit Strategy')

    class Meta:
        ordering = ["id"]

    def __str__(self) -> str:
        return str(self.name[:20])

class ReviewMeetingNote(BaseModel):
    '''Model to store data about review meeting notes from teacher and SST'''
    strategy = models.ManyToManyField(
        ImplicitStrategy, related_name='strategy_name')
    text_strategy = models.CharField(
        verbose_name='Other strategy', max_length=2000, blank=True, null=True)
    notes = models.CharField(
        verbose_name='Anectodal notes', max_length=2000)
    YES = 'Y'
    NO = 'N'
    PROGRESS_CHOICES = [
        (YES, 'Yes'),
        (NO, 'No')
    ]
    progress = models.CharField(
        max_length=1, choices=PROGRESS_CHOICES, default=YES, verbose_name='Progress')
    user = models.ForeignKey(MyUser,
                             on_delete=models.PROTECT)
    stream = models.ForeignKey(Stream, on_delete=models.CASCADE, 
                                verbose_name='Stream review', related_name='student_stream')
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name='review_student', default=None)

    class Meta:
        ordering = ['id']

    def __str__(self) -> str:
        return str(self.id)
