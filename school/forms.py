from django.forms import DateInput, ModelForm
from .models import MyUser, NotesPTS, Consern, Intake, Observation, Support, OcupationalTherapy, SpeechTherapy
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
            'username': forms.TextInput(attrs={'class':'form-control'}),
            'password': forms.PasswordInput(attrs={'class':'form-control'})
        }

class UploadExcelFileForm(forms.Form):
    '''form to upload students'''
    file = forms.FileField()

# class NotesPTSForm(ModelForm):
#     class Meta:
#         model = NotesPTS
#         fields = ['date', 'note']
#         exclude = ['student']

#         labels = {
#             'date': _('Pick a date'),
#             'note': _('Add note')
#                 }
#         widgets = {
#             'date': forms.DateInput(attrs={'class':'form-control', 'type':'date'}),
#             'note': forms.TextInput(attrs={'class':'form-control'})
#         }

class ConsernForm(ModelForm):
    date = forms.DateField(
        required=True,
        widget=forms.widgets.DateInput(
            attrs={
                "placeholder": "Add date ...",
                "class": "form-control",
                'type':'date'
            }
        ), 
        label="Date",
    )
    consern_type = forms.CharField(
        required=True,
        widget=forms.widgets.TextInput(
            attrs={
                "placeholder": "Add type of Concern",
                "class": "form-control",
            }
        ),
        label="Type of Concern",
    )
    
    consern_type = forms.CharField(
        required=True,
        widget=forms.widgets.TextInput(
            attrs={
                "placeholder": "Add type of Concern",
                "class": "form-control",
            }
        ),
        label="Type of Concern",
    )

    refers = forms.ChoiceField(
        required=True,
        widget=forms.widgets.Select(
            attrs={
                "class": "form-control",
            }
        ),
        choices = Consern.CONSERN_CHOICES
    )
    
    class Meta:
        model = Consern
        exclude = ['student', 'teacher']
        labels = {
            # 'date': _('Date'),
            # 'consern_type': _('Type of Concern'),
            'strategy_used': _('Strategies Used'),
            'num_weeks': _('Number of weeks'),
            'st_responce': _('Student Response'),
            'teach_comm': _('Teacher Comments'),
            'refers': _('Referral')
            }

        widgets = {
            # 'date': forms.DateInput(attrs={'class':'form-control', 'type':'date'}),
            # 'consern_type': forms.TextInput(attrs={'class':'form-control'}),
            'strategy_used': forms.TextInput(attrs={'class':'form-control', 'placeholder':'custom'}),
            'num_weeks': forms.NumberInput(attrs={'class':'form-control', 'placeholder':'any???'}),
            'st_responce': forms.TextInput(attrs={'class':'form-control', 'placeholder':'any???'}),
            'teach_comm': forms.TextInput(attrs={'class':'form-control', 'placeholder':'any???'}),
            # 'refers': forms.ChoiceField(choices=Consern.CONSERN_CHOICES),
        }

class IntakeForm(ModelForm):
    timeline = forms.IntegerField(
        required=False,
        widget=forms.widgets.NumberInput(
            attrs={
                "placeholder": "TODO ask...",
                "class": "form-control",
                'type':'number',
                
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
                'type':'text'
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
        choices = Intake.BEHAVE_CHOICES,
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

    what_done = forms.CharField(
        required=False,
        widget=forms.widgets.TextInput(
            attrs={
                "placeholder": 'Refer to the tools listed in your Teacher Three'
                                'Stream Binder',
                "class": "form-control",
                'type': 'text'
            }
        ), 
        label='''What have you done to help alleviate or work through these 
                concerning patterns''',
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
        label= 'What response level do you believe the student is currently in? '
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
        label = 'Support text',
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
        # fields = ['date', 'support_text', 'support_note']
        exclude = ['teacher', 'sst', 'student']


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

