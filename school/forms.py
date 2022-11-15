from django.forms import ModelForm
from .models import (MyUser,
                     Intake,
                     Support,
                     OcupationalTherapy,
                     SpeechTherapy,
                     ResponceToSupport,
                     ReadingScreening,
                     ReviewMeetingNote,
                     ImplicitStrategy,
                     SupportName
                     )
from django.utils.translation import gettext_lazy as _
from django import forms


class MyUserForm(ModelForm):
    class Meta:
        model = MyUser
        fields = ['username', 'password']
        labels = {
            'username': _('Username'),
            'password': _('Password')
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'})
        }


class UploadExcelFileForm(forms.Form):
    '''form to upload data from excel files'''
    file = forms.FileField()


class IntakeForm(ModelForm):
    timeline = forms.IntegerField(
        required=False,
        widget=forms.widgets.NumberInput(
            attrs={
                "placeholder": "TODO ask...",
                "class": "form-control",
                'type': 'number',

            }
        ),
        label="How long has the student been with you?"
    )

    sst_reasoning = forms.CharField(
        required=False,
        widget=forms.widgets.TextInput(
            attrs={
                "placeholder": "One sentence...",
                "class": "form-control",
                'type': 'text'
            }
        ),
        label='''In one sentence, why did you bring this child to the 
                attention of the SST?'''
    )

    behavior_patterns = forms.CharField(
        required=False,
        widget=forms.widgets.Textarea(
            attrs={
                "placeholder": 'Please use the following format. EXAMPLE: Ever'
                'since (Date), I have observed that (Child) does'
                '(Behavior/Concern) when ',
                "class": "form-control",
                'type': 'text',
                'rows': '3'
            }
        ),
        label="What are the primary behavior patterns that you are concerned about?",
    )

    behavior_quality = forms.ChoiceField(
        required=False,
        widget=forms.widgets.Select(
            attrs={
                "class": "form-control",
            }
        ),
        choices=Intake.BEHAVE_CHOICES,
        label='How would you qualify this behavior? Please choose one: ',
    )

    why_consern = forms.CharField(
        required=False,
        widget=forms.widgets.TextInput(
            attrs={
                "placeholder": "Describe your conserns...",
                "class": "form-control",
                'type': 'text'
            }
        ),
        label="Why is this concerning to you?",
    )

    what_done = forms.CharField(
        required=False,
        widget=forms.widgets.TextInput(
            attrs={
                "placeholder": '''Refer to the tools listed in your Teacher 
                                Three Stream Binder''',
                "class": "form-control",
                'type': 'text'
            }
        ),
        label='What have you done to help alleviate or work through'
        'these concerning patterns',
    )

    smal_done = forms.CharField(
        required=False,
        widget=forms.widgets.Textarea(
            attrs={
                "placeholder": "",
                "class": "form-control",
                'type': 'text',
                'rows': '3'
            }
        ),
        label="What have you done that has worked, even to a small extent?",
    )

    didnt_worked = forms.CharField(
        required=False,
        widget=forms.widgets.Textarea(
            attrs={
                "placeholder": "",
                "class": "form-control",
                'type': 'text',
                'rows': '3'
            }
        ),
        label="What have you done that has not worked or shown no positive change?",
    )

    worse = forms.CharField(
        required=False,
        widget=forms.widgets.Textarea(
            attrs={
                "placeholder": "",
                "class": "form-control",
                'type': 'text',
                'rows': '3'
            }
        ),
        label="What have you done that has made things worse?",
    )

    response_level = forms.CharField(
        required=False,
        widget=forms.widgets.Textarea(
            attrs={
                "placeholder": "(Attach incident report)?",
                "class": "form-control",
                'type': 'text',
                'rows': '3'
            }
        ),
        label='What response level do you believe the student is currently in? '
        'Have there been any threshold events that require an immediate'
        'response (Attach incident report)?',
    )

    other_info = forms.CharField(
        required=False,
        widget=forms.widgets.Textarea(
            attrs={
                "placeholder": "(Attach incident report)?",
                "class": "form-control",
                'type': 'text',
                'rows': '3'
            }
        ),
        label='''What other pieces of information would it be helpful for the SST
                 to have when deciding on how to move forward with your student?''',
    )

    estim_result = forms.CharField(
        required=False,
        widget=forms.widgets.Textarea(
            attrs={
                "placeholder": "",
                "class": "form-control",
                'type': 'text',
                'rows': '3'
            }
        ),
        label='''What would you like to see out of this process for your student?''',
    )

    class Meta:
        model = Intake
        exclude = ['student', 'teacher', 'concern']


class SupportForm(ModelForm):
    support = forms.ModelMultipleChoiceField(
        required=True,
        queryset=SupportName.objects.all(),
        widget=forms.widgets.SelectMultiple(
            attrs={
                "class": "form-control",
            }
        ),
        label='Supports from SST strategy',
        # help_text = 'Hold Shift button on your keyboard and choose more than one strategy'
    )
    date = forms.DateField(
        required=True,
        widget=forms.widgets.DateInput(
            attrs={
                "class": "form-control",
                "type": "date"
            }
        ),
        label="Support date",
    )
    suport_text = forms.CharField(
        required=True,
        widget=forms.widgets.Textarea(
            attrs={
                "placeholder": "TODO: Do we have any plaseholder?",
                "class": "form-control",
                "type": "text",
                "rows": '2'
            }
        ),
        label='Support text',
    )

    note = forms.CharField(
        required=True,
        widget=forms.widgets.Textarea(
            attrs={
                "placeholder": "TODO: Do we have any plaseholder?",
                "class": 'form-control',
                'type': 'text',
                "rows": '3'
            }
        ),
        label='Support note'
    )

    class Meta:
        model = Support
        exclude = ['created_at', 'updated_at', 'teacher', 'sst', 'student', 'stream']


class OcupationalTherapyForm(ModelForm):
    screen_date = forms.DateField(
        required=True,
        widget=forms.widgets.DateInput(
            attrs={
                "class": "form-control",
                "type": "date"
            }
        ),
        label="Screen date",
    )
    screen_time = forms.TimeField(
        required=True,
        widget=forms.widgets.TimeInput(
            attrs={
                "class": "form-control",
                "type": "time"
            }
        ),
        label="Screen time (e.g. 05.00 PM)",
    )
    full_screen_recom = forms.CharField(
        required=True,
        widget=forms.widgets.Textarea(
            attrs={
                "placeholder": "TODO: Do we have any plaseholder?",
                "class": 'form-control',
                'type': 'text',
                "rows": '3'
            }
        ),
        label='Full Screening Recommended?'
    )
    notes = forms.CharField(
        required=True,
        widget=forms.widgets.Textarea(
            attrs={
                "placeholder": "TODO: Do we have any plaseholder?",
                "class": 'form-control',
                'type': 'text',
                "rows": '3'
            }
        ),
        label='Note'
    )

    class Meta:
        model = OcupationalTherapy
        # exclude = ['teacher', 'student', 'created_at', 'updated_at']
        fields = ['screen_date', 'screen_time', 'full_screen_recom', 'notes']


class SpeechTherapyForm(ModelForm):
    screen_date = forms.DateField(
        required=True,
        widget=forms.widgets.DateInput(
            attrs={
                "class": "form-control",
                "type": "date"
            }
        ),
        label="Screen date",
    )
    add_notes = forms.CharField(
        required=True,
        widget=forms.widgets.Textarea(
            attrs={
                "placeholder": "TODO: Do we have any plaseholder?",
                "class": 'form-control',
                'type': 'text',
                "rows": '3'
            }
        ),
        label='Additional Notes'
    )
    scr_res = forms.CharField(
        required=True,
        widget=forms.widgets.Textarea(
            attrs={
                "placeholder": "TODO: Do we have any plaseholder?",
                "class": 'form-control',
                'type': 'text',
                "rows": '3'
            }
        ),
        label='Screening Results / Recommendations'
    )

    class Meta:
        model = SpeechTherapy
        fields = ['screen_date', 'add_notes', 'scr_res']


class ResponceToSupportForm(ModelForm):
    date = forms.DateField(
        required=True,
        widget=forms.widgets.DateInput(
            attrs={
                'class': 'form-control',
                'type': 'date'
            }
        ),
        label='Response date'
    )

    intervention = forms.CharField(
        required=True,
        widget=forms.widgets.Textarea(
            attrs={
                'placeholder': 'Do we have any placeholder?',
                'class': 'form-control',
                'type': 'text',
                'rows': 2
            }
        ),
        label='Intervetion'
    )

    note = forms.CharField(
        required=True,
        widget=forms.widgets.Textarea(
            attrs={
                'placeholder': 'Do we have any placeholder?',
                'class': 'form-control',
                'type': 'text',
                'rows': 2
            }
        ),
        label='Please, provide some notes...'
    )

    class Meta:
        model = ResponceToSupport
        fields = ['date', 'intervention', 'note']


class ReadingScreeningForm(ModelForm):
    date_screen = forms.DateField(
        required=True,
        widget=forms.widgets.DateInput(
            attrs={
                'class': 'form-control',
                'type': 'date'
            }
        ),
        label='Screening date'
    )

    screen_type = forms.ChoiceField(
        required=True,
        widget=forms.widgets.Select(
            attrs={
                'class': 'form-control'
            }
        ),
        choices=ReadingScreening.READING_CHOISES,
        label='Select type of screening',
    )
    errors_screen = forms.CharField(
        required=True,
        widget=forms.widgets.TextInput(
            attrs={
                'placeholder': '3 decoding errors; 2 minor/1 significant',
                'class': 'form-control',
                'type': 'text',
            }
        ),
        label='Describe errors happened during the screening'
    )

    question_screen = forms.CharField(
        required=True,
        widget=forms.widgets.TextInput(
            attrs={
                'placeholder': '7-8/10 comprehesion questions',
                'class': 'form-control',
                'type': 'text',
            }
        ),
        label='Describe results of questions'
    )
    notes = forms.CharField(
        required=True,
        widget=forms.widgets.Textarea(
            attrs={
                'placeholder': 'Recomendations, notes, additional information',
                'class': 'form-control',
                'type': 'text',
                'rows': 2
            }
        ),
        label='Do you have any recomendations or notes?'
    )

    class Meta:
        model = ReadingScreening
        fields = ['date_screen', 'screen_type',
                  'errors_screen', 'question_screen', 'notes']


class ReviewMeetingNoteForm(forms.Form):
    strategy = forms.ModelMultipleChoiceField(
        required=True,
        queryset=ImplicitStrategy.objects.all(),
        widget=forms.widgets.SelectMultiple(
            attrs={
                "class": "form-control",
            }
        ),
        label='Implicit strategy',
        help_text = 'Hold Shift button on your keyboard and choose more than one strategy'
    )
    text_strategy = forms.CharField(
        required=False,
        widget=forms.widgets.Textarea(
            attrs={
                'placeholder': 'Add custom strategies, if used. ',
                'class': 'form-control',
                'type': 'text',
                'rows': '3'
            }
        ),
        label='Custom strategy',
    )
    notes = forms.CharField(
        required=True,
        widget=forms.widgets.Textarea(
            attrs={
                'placeholder': 'Add custom strategies, if used. ',
                'class': 'form-control',
                'type': 'text',
                'rows': '3'
            }
        ),
        label='Anectodal notes',
    )
    progress = forms.ChoiceField(
        required=True,
        widget=forms.widgets.Select(
            attrs={
                "class": "form-control",
            }
        ),
        choices= [('','Choose YES or NO')] + ReviewMeetingNote.PROGRESS_CHOICES,
        label='Has the student made sufficient progress?',
    )


class ReviewMeetingNoteFormModel(forms.ModelForm):
    strategy = forms.ModelMultipleChoiceField(
        required=True,
        queryset=ImplicitStrategy.objects.all(),
        widget=forms.widgets.SelectMultiple(
            attrs={
                "class": "form-control",
            }
        ),
        label='Implicit strategy',
        help_text = 'Hold Shift button on your keyboard and choose more than one strategy'
    )
    text_strategy = forms.CharField(
        required=False,
        widget=forms.widgets.Textarea(
            attrs={
                'placeholder': 'Add custom strategies, if used. ',
                'class': 'form-control',
                'type': 'text',
                'rows': '3'
            }
        ),
        label='Custom strategy',
    )
    notes = forms.CharField(
        required=True,
        widget=forms.widgets.Textarea(
            attrs={
                'placeholder': 'Add custom strategies, if used. ',
                'class': 'form-control',
                'type': 'text',
                'rows': '3'
            }
        ),
        label='Anectodal notes',
    )
    progress = forms.ChoiceField(
        required=True,
        widget=forms.widgets.Select(
            attrs={
                "class": "form-control",
            }
        ),
        choices= [('','Choose YES or NO')] + ReviewMeetingNote.PROGRESS_CHOICES,
        label='Has the student made sufficient progress?',
    )

    class Meta:
        model = ReviewMeetingNote
        fields = ['strategy', 'text_strategy', 'notes', 'progress',]
