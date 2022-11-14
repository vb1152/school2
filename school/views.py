'''Django views'''

import json
from django.views import View
from django.views.generic.edit import CreateView
from django.views.generic import DetailView

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin


from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist

from django.urls import reverse_lazy

from datetime import datetime, timedelta, date

from .utils import (SstCheckMixin, TeacherCheckMixin,
                    StaffCheckMixin,
                    )

from .models import (Intake, NotesPTS,
                     Student, MyUser, Observation,
                     Support, OcupationalTherapy,
                     SpeechTherapy, ResponceToSupport,
                     ReadingScreening, Stream, ReviewMeetingNote
                     )
from .forms import (MyUserForm, UploadExcelFileForm,
                    IntakeForm, SupportForm, OcupationalTherapyForm,
                    SpeechTherapyForm, ResponceToSupportForm,
                    ReadingScreeningForm, ReviewMeetingNoteForm
                    )
from .utils import (read_excel_with_students,
                    calculate_age, sst_check,
                    teacher_check, staff_check,
                    read_excel_save_users,
                    create_sample_excel_users,
                    create_sample_excel_students
                    )


# Create your views here.
def index(request):
    '''Index function.'''
    return render(request, 'school/index.html')


def login_view(request):
    '''Login view'''
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        # check authentication
        if user is not None:
            login(request, user)
            if user.is_teacher is True:  # redirect to a teacher page
                return HttpResponseRedirect(reverse('school:teacher_view'))
            if user.is_sst is True:
                return HttpResponseRedirect(reverse('school:sst_view'))
            if user.is_staff:
                return HttpResponseRedirect(reverse('school:staff_view'))
            return HttpResponseRedirect(reverse('school:index'))

        messages.error(request, 'Wrong username and/or password')
        return HttpResponseRedirect(reverse('school:login'))

    user_form = MyUserForm()
    context = {
        'form': user_form
    }
    return render(request, 'school/login.html', context)


def logout_view(request):
    '''Logout view'''
    logout(request)
    return HttpResponseRedirect(reverse('school:index'))


@user_passes_test(teacher_check)
def teacher_view(request):
    '''Teacher view'''
    # get list of students for one teacher
    students = Student.objects.filter(
        teacher=request.user).select_related('teacher')
    streams = Stream.objects.filter(
        teacher=request.user, date_review__gte=datetime.now())
    context = {
        'students': students,
        'streams': streams
    }
    return render(request, 'school/teacher.html', context)


@user_passes_test(staff_check)
def upload_students(request):
    '''Save student to the data base '''
    if request.method == 'POST':
        form = UploadExcelFileForm(request.POST, request.FILES)
        if form.is_valid():
            result, message = read_excel_with_students(request.FILES['file'])
            messages.success(request, f'Saved {result} students profiles!')
            return HttpResponseRedirect(reverse('school:staff_view'))
        else:
            messages.error(request, 'Something wrong')
            return HttpResponseRedirect(reverse('school:staff_view'))


@login_required
def student_data_profile(request, **kwargs):
    '''Function to show student data profile for a teacher'''
    if request.method == 'GET':
        student = get_object_or_404(Student, id=kwargs['stud_id'])
        age_years, age_months = calculate_age(str(student.date_of_birth))
        supports = Support.objects.filter(
            student=student).select_related('sst')

        stream = Stream.objects.get(id=4)
        # stream.next_streams()
        print(stream.next_streams())


        context = {
            'student': student,
            'age_years': age_years,
            'age_months': age_months,
            'supports': supports,
        }

        return render(request, 'school/teacher/student_profile.html', context)

                                #    <!-- {{ stream.reviewmeetingnote.all }} -->
                                #     {% for rev in stream.student_stream.all %}
                                #         {{ rev.progress }}
                                #     {% endfor %}

@user_passes_test(teacher_check)
def save_note_from_PTC(request):
    if request.method == 'POST':
        note = json.load(request)
        student = Student.objects.get(id=note['stud_id'])
        note_inst = NotesPTS(
            student=student, date=note['note_date'], note=note['note_text'])
        note_inst.save()
        # {'note_date': '2022-07-26', 'note_text': 'ads', 'stud_id': '5'}

        all_notes = NotesPTS.objects.filter(student=student).values()
        data = {'notes': list(all_notes), }
        return JsonResponse(data, safe=False)


@user_passes_test(teacher_check)
def make_review(request, *, stud_id, stream_id):
    '''View to get a form for a Review Meeting Notex
    for a teacher.'''
    if request.method == 'GET':
        review_form = ReviewMeetingNoteForm()
        student = Student.objects.get(id=stud_id)
        stream = Stream.objects.get(id=stream_id)
        intake_form = IntakeForm()
        context = {
            'student': student,
            'stream_id': stream.id,
            'review_form': review_form,
            'intake_form': intake_form,
        }
        return render(request, 'school/teacher/review_note.html', context)

@user_passes_test(teacher_check)
def make_review_post(request):
    '''Save review note from a teacher'''
    if request.method == 'POST':
        review_form = ReviewMeetingNoteForm(request.POST)
        intake_form = IntakeForm(request.POST)
        student = Student.objects.get(id=request.POST['stud_id'])
        stream_first = Stream.objects.get(id=request.POST['stream_id'])
        
        if review_form.is_valid():
            new_review = ReviewMeetingNote()
            new_review.text_strategy = review_form.cleaned_data['text_strategy']
            new_review.notes = review_form.cleaned_data['notes']
            new_review.progress = review_form.cleaned_data['progress']
            new_review.stream = stream_first
            new_review.student = student
            new_review.user = request.user
            new_review.save()
            new_review.strategy.set(review_form.cleaned_data['strategy'])

            if review_form.cleaned_data['progress'] == 'Y':
                stream_first.status = Stream.CLOSED
                stream_first.progress = Stream.YES

                new_start = stream_first.date_review + timedelta(days=1)
                new_review = new_start + timedelta(days=21)

                stream = Stream(
                    name = stream_first.name,
                    student=student,
                    teacher = request.user,
                    date_start = new_start,
                    date_review = new_review,
                    stream_prev = stream_first
                )
                stream.save()
            
            if intake_form.is_valid() and 'timeline' in request.POST and 'sst_reasoning' in request.POST:
                new_intake = intake_form.save(commit=False)
                new_intake.student = student
                new_intake.teacher = request.user
                new_intake.save()
                # add intake form to a stream
                stream_first.intake = new_intake
                stream_first.save()

                # Create new stream with level 2,
                stream_intake = Stream(
                    name = stream_first.name,
                    student=stream_first.student,
                    teacher = request.user,
                    date_start = stream_first.date_review + timedelta(days=1),
                    date_review = stream_first.date_review + timedelta(days=22),
                    level = '2',
                    stream_prev = stream_first
                )
                stream_intake.save()

                messages.success(
                request, 'Thank you! Review Note and Intake data is saved!')
                return HttpResponseRedirect(reverse('school:student_data_profile',
                                                    args=[student.id]))
            stream_first.save()
            messages.success(request, 'Thank you! Review is saved!')
            return HttpResponseRedirect(reverse('school:student_data_profile', args=[request.POST['stud_id']]))


@user_passes_test(teacher_check)
def make_consern(request, *, stud_id, stream_id):
    '''View for making a concern'''
    pass
    # def update_get(request, *, pk):
    # if request.method == 'GET':
    #     # print('make concern GET', stud_id, stream_id)
    #     student = Student.objects.get(id=stud_id)
    #     stream = Stream.objects.get(id=stream_id)
    #     cons_form = ConsernForm()
    #     intake_form = IntakeForm()
    #     context = {
    #         'student': student,
    #         'cons_form': cons_form,
    #         'intake_form': intake_form,
    #         'stream_id': stream.id
    #     }
    #     return render(request, 'school/consern.html', context)

# @user_passes_test(teacher_check, sst_check)
# def read_concern(request, *, concern_id):
#     if request.method == 'GET':
#         concern = Consern.objects.get(id=concern_id)
#         context = {
#             'concern': concern
#         }
#         return render(request, 'school/teacher/consern_view_teacher.html', context)

# ShowConcernTeacher
class ShowReviewTeacher(TeacherCheckMixin, DetailView):
    model = ReviewMeetingNote
    template_name = 'school/teacher/review_view_teacher.html'
    login_url = 'login'

class ShowIntakeTeacher(TeacherCheckMixin, DetailView):
    model = Intake
    template_name = 'school/teacher/intake_view_teacher.html'
    login_url = 'login'

class ShowReviewSST(SstCheckMixin, DetailView):
    model = ReviewMeetingNote
    template_name = 'school/sst/review_view_sst.html'
    login_url = 'login'

class ShowIntakeSST(SstCheckMixin, DetailView):
    model = Intake
    template_name = 'school/sst/intake_view_sst.html'
    login_url = 'login'

@user_passes_test(teacher_check)
def make_consern_post(request):
    '''Function to save concern and intake forms to database.'''
    pass
    # if request.method == 'POST':

    #     cons_form = ConsernForm(request.POST)
    #     intake_form = IntakeForm(request.POST)

    #     student = Student.objects.get(id=request.POST['stud_id'])
    #     teacher = MyUser.objects.get(id=request.user.id)

    #     stream_first = Stream.objects.get(id=request.POST['stream_id'])
    #     # save concern and change status of the stream
    #     if cons_form.is_valid():
    #         new_concern = cons_form.save(commit=False)
    #         new_concern.student = student
    #         new_concern.teacher = teacher
    #         new_concern.save()
    #         # add concern form to a stream
    #         stream_first.concern = new_concern

    #         if new_concern.refers == 'RES':
    #             stream_first.status = 'CL'

    #             new_start = stream_first.date_review + timedelta(days=1)
    #             new_review = new_start + timedelta(days=21)

    #             stream = Stream(
    #                 name = stream_first.name,
    #                 student=student,
    #                 teacher = request.user,
    #                 date_start = new_start,
    #                 date_review = new_review,
    #                 stream_prev = stream_first
    #             )
    #             stream.save()

    #         # create new stream with three weeks and red status
    #         if intake_form.is_valid() and 'timeline' in request.POST and 'sst_reasoning' in request.POST:

    #             new_intake = intake_form.save(commit=False)
    #             new_intake.student = student
    #             new_intake.teacher = teacher
    #             new_intake.concern = new_concern
    #             new_intake.save()
    #             # add intake form to a stream
    #             stream_first.intake = new_intake
    #             stream_first.save()

    #             # Create new stream with level 2,
    #             # now_date = datetime.now()
    #             # review_date = now_date + timedelta(days=21)

    #             # stream_first.date_review 2022-11-15 <class 'datetime.date'>
    #             stream_intake = Stream(
    #                 name = stream_first.name,
    #                 student=stream_first.student,
    #                 teacher = request.user,
    #                 date_start = stream_first.date_review + timedelta(days=1),
    #                 date_review = stream_first.date_review + timedelta(days=22),
    #                 level = '2'
    #             )
    #             stream_intake.save()

    #             messages.success(
    #                 request, 'Thank you! Concern and Intake data is saved!')
    #             return HttpResponseRedirect(reverse('school:student_data_profile',
    #                                                 args=[student.id]))

    #         stream_first.save()

    #         messages.success(request, 'Thank you! Concern is saved!')
    #         return HttpResponseRedirect(reverse('school:student_data_profile', args=[student.id]))

    #     messages.error(request, 'Some error. Concern is not saved.')
    #     return HttpResponseRedirect(reverse('school:student_data_profile',
    #                                 args=[request.POST['stud_id']]))


@user_passes_test(sst_check)
def sst_view(request):
    '''Function to show main page for SST'''
    if request.method == 'GET':
        students = Student.objects.all().select_related('teacher')
        streams = Stream.objects.all()
        context = {
            'students': students,
            'streams': streams
        }

        return render(request, 'school/sst.html', context)


@user_passes_test(sst_check)
def save_observation(request):
    '''Function to save observation from SST team
    via fetch api call'''
    if request.method == 'POST':
        observ_data = json.load(request)
        observation = Observation(
            date=observ_data['obs_date'],
            note=observ_data['obs_text'],
            teacher=MyUser.objects.get(id=observ_data['teach_id']),
            student=Student.objects.get(id=observ_data['stud_id']),
            stream = Stream.objects.get(id=observ_data['stream_id']),
            sst=request.user
        )
        observation.save()
        data = {'status': 200}
        return JsonResponse(data, safe=False)


@user_passes_test(sst_check)
def support(request, **kwargs):
    pass
    # if request.method == 'GET':
    #     concern = Consern.objects.select_related(
    #         'student').get(id=kwargs['conc_id'])
    #     support_form = SupportForm()
    #     context = {
    #         'support_form': support_form,
    #         'concern': concern,
    #     }
    #     return render(request, 'school/support.html', context)


@user_passes_test(sst_check)
def make_support_post(request):
    if request.method == "POST":
        support_form = SupportForm(request.POST)
        if support_form.is_valid():
            student = Student.objects.get(id=request.POST['stud_id'])
            teacher = MyUser.objects.get(id=request.POST['teach_id'])
            # concern = Consern.objects.get(id=request.POST['cons_id'])
            sst = request.user
            new_support = support_form.save(commit=False)
            new_support.student = student
            new_support.sst = sst
            new_support.teacher = teacher
            # new_support.concern = concern
            new_support.save()

            messages.success(request, 'Thank you! Support note is saved!')
            return HttpResponseRedirect(reverse('school:sst_view'))


@user_passes_test(staff_check)
def staff_view(request):
    '''Function for main page for user with is_staff rights'''
    if request.method == 'GET':
        excel_form = UploadExcelFileForm()
        context = {
            'file_form': excel_form
        }
        return render(request, 'school/staff.html', context)




@user_passes_test(teacher_check)
def update_concern(request):
    '''Function to update concern form and intake forms'''
    pass
    # if request.method == 'GET':
    #     # concern = Consern.objects.get(id=request.GET['concern_id'])
    #     concern_form = ConsernForm(instance=concern)
    #     student = concern.student

    #     try:
    #         intake_form = IntakeForm(instance=concern.consern_intake)
    #         context = {
    #             # 'concern': concern,
    #             'concern_form': concern_form,
    #             'intake_form': intake_form,
    #             'student': student
    #         }
    #     # if concern doesn have an intake form
    #     except ObjectDoesNotExist:
    #         intake_form = IntakeForm()
    #         for fieldname in intake_form.fields:
    #             intake_form.fields[fieldname].disabled = True

    #         context = {
    #             'concern': concern,
    #             'concern_form': concern_form,
    #             'intake_form': intake_form,
    #             'student': student
    #         }
    #     return render(request, 'school/update_concern.html', context)

    # if request.method == 'POST':
    #     # concern = Consern.objects.get(id=request.POST['concern_id'])
    #     concern_form = ConsernForm(request.POST, instance=concern)

    #     # update current Intake data
    #     if 'timeline' in request.POST and 'sst_reasoning' in request.POST:
    #         # means that intake form are filled and data sent
    #         try:
    #             intake = Intake.objects.get(concern=concern)
    #             intake_form = IntakeForm(request.POST, instance=intake)
    #             if intake_form.has_changed():
    #                 intake_form.save()
    #                 if concern_form.has_changed():
    #                     concern_form.save()
    #                     # case: concern and intake forms updated
    #                     messages.success(
    #                         request, 'Thank you! Concern updates and Intake updates is saved!')
    #                     return HttpResponseRedirect(reverse('school:student_data_profile', args=[concern.student.id]))
    #                 # case: intake forms updated
    #                 messages.success(
    #                     request, 'Thank you! Intake updates is saved!')
    #                 return HttpResponseRedirect(reverse('school:student_data_profile', args=[concern.student.id]))
    #         except ObjectDoesNotExist:
    #             # case when update Concern form and ADD intake form
    #             if concern_form.has_changed():
    #                 concern_form.save()

    #             intake_form = IntakeForm(request.POST)
    #             if intake_form.is_valid():
    #                 new_intake = intake_form.save(commit=False)
    #                 new_intake.student = concern.student
    #                 new_intake.teacher = concern.teacher
    #                 new_intake.concern = concern
    #                 new_intake.save()

    #                 messages.success(
    #                     request, 'Thank you! Intake form added to the Concern!')
    #                 return HttpResponseRedirect(reverse('school:student_data_profile', args=[concern.student.id]))

    # # case only concern form updated.
    # if concern_form.has_changed():
    #     concern_form.save()
    #     messages.success(request, 'Thank you! Concern data is updated!')
    #     return HttpResponseRedirect(reverse('school:student_data_profile', args=[concern.student.id]))
    # else:
    #     messages.info(request, 'No changes in Concern data are detected.')
    #     return HttpResponseRedirect(reverse('school:student_data_profile', args=[concern.student.id]))


@user_passes_test(teacher_check)
def ocupational_therapy(request, *, stud_id):
    '''Function to open OcupationalTherapyForm'''
    if request.method == 'GET':
        student = Student.objects.get(id=stud_id)
        ocup_therap_form = OcupationalTherapyForm()
        context = {
            'ocup_therap_form': ocup_therap_form,
            'student': student
        }
        return render(request, 'school/occup_therap.html', context)


@user_passes_test(teacher_check)
def ocupational_therapy_post(request):
    '''Function to save data from Ocupational Therapy Form'''
    if request.method == 'POST':
        ocup_therap_form = OcupationalTherapyForm(request.POST)
        if ocup_therap_form.is_valid():
            student = Student.objects.get(id=request.POST['stud_id'])
            new_ocup = ocup_therap_form.save(commit=False)
            new_ocup.student = student
            new_ocup.teacher = request.user
            new_ocup.save()

            messages.success(
                request, 'Thank you! Occupational Therapy service data  is saved.')
            return HttpResponseRedirect(reverse('school:student_data_profile', args=[student.id]))


@user_passes_test(teacher_check)
def speech_therapy(request, *, stud_id):
    '''Function to show SpeechTherapyForm for the user'''
    if request.method == 'GET':
        student = Student.objects.get(id=stud_id)
        speech_form = SpeechTherapyForm()
        context = {
            'student': student,
            'speech_form': speech_form
        }
        return render(request, 'school/speech_therap.html', context)


@user_passes_test(teacher_check)
def speech_therapy_post(request):
    '''Function to save result of Speech Therapy'''
    if request.method == 'POST':
        speech_form = SpeechTherapyForm(request.POST)
        if speech_form.is_valid():
            student = Student.objects.get(id=request.POST['stud_id'])
            new_speech_ther = speech_form.save(commit=False)
            new_speech_ther.teacher = request.user
            new_speech_ther.student = student
            new_speech_ther.save()

            messages.success(
                request, 'Thank you! Speech Therapy results are saved!')
            return HttpResponseRedirect(reverse('school:student_data_profile', args=[student.id]))


@user_passes_test(staff_check)
def upload_users(request):
    if request.method == 'POST':
        saved_users = read_excel_save_users(request)

        messages.success(request, f'Saved {saved_users} users profiles!')
        return HttpResponseRedirect(reverse('school:staff_view'))

    messages.error(request, 'Some error. Sorry')
    return HttpResponseRedirect(reverse('school:staff_view'))


class ShowObservationTextSstView(SstCheckMixin, DetailView):
    model = Observation
    template_name = 'school/sst/show_observation_text_sst.html'
    login_url = 'login'


class ReadSupportSstView(SstCheckMixin, DetailView):
    'View to show support data to sst'
    model = Support
    template_name = 'school/sst/show_support_text_sst.html'
    login_url = 'login'


class ShowReadScreen(LoginRequiredMixin, DetailView):
    '''View to show results of reading screening'''
    model = ReadingScreening
    template_name = 'school/teacher/show_read_screen.html'
    login_url = 'login'


class ReadingScreenView(TeacherCheckMixin, CreateView):
    'Save result of reading screening'
    model = ReadingScreening
    template_name = 'school/teacher/create_read_screen.html'
    form_class = ReadingScreeningForm
    login_url = 'login'

    # save data in db
    def form_valid(self, form) -> HttpResponse:
        form.instance.teacher = self.request.user
        form.instance.student = Student.objects.get(id=self.kwargs['stud_id'])
        return super().form_valid(form)

    def get_success_url(self) -> str:
        messages.success(self.request,
                         'Thank you! Reading screening results are saved!')
        return reverse('school:student_data_profile', args=(self.kwargs['stud_id'],))

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['student'] = Student.objects.get(id=self.kwargs['stud_id'])
        return context


class ShowObservation(LoginRequiredMixin, DetailView):
    '''View to show observations from student profile 
    for all users with login'''
    model = Observation
    template_name = 'school/teacher/show_observation.html'
    login_url = 'login'


class ShowNote(LoginRequiredMixin, DetailView):
    '''View to show note from teacher conference with parents'''
    model = NotesPTS
    template_name = 'school/teacher/show_note.html'
    login_url = 'login'


class ShowSupport(TeacherCheckMixin, DetailView):
    '''Class show support and responses from a teacher'''
    model = Support
    template_name = 'school/teacher/show_support.html'
    login_url = 'login'


class ShowOcupTherapy(TeacherCheckMixin, DetailView):
    '''Show results of Occupational therapy'''
    model = OcupationalTherapy
    template_name = 'school/teacher/speech_ocup_results.html'
    login_url = 'login'


class ShowSpeechTherapy(TeacherCheckMixin, DetailView):
    '''Show results of speech therapy'''
    model = SpeechTherapy
    template_name = 'school/teacher/speech_therap_results.html'
    login_url = 'login'


class CreateResponse(TeacherCheckMixin, CreateView):
    '''Save response to support from a teacher.'''
    model = ResponceToSupport
    template_name = 'school/teacher/create_responce.html'
    form_class = ResponceToSupportForm
    login_url = 'login'

    # save data from a form
    def form_valid(self, form) -> HttpResponse:
        form.instance.support = Support.objects.get(pk=self.kwargs['supp_pk'])
        # print(self.kwargs)   {'stud_id': 38, 'supp_pk': 3}
        return super().form_valid(form)

    # redirect to student profile
    def get_success_url(self):
        messages.success(self.request, 'Thank you! Your response is saved')
        return reverse('school:student_data_profile', args=(self.kwargs['stud_id'],))

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)  # call super
        # add to the returned dictionary
        context['responce'] = ResponceToSupport.objects.filter(
            support=self.kwargs['supp_pk'])
        # context['responce'] = ResponceToSupport.objects.all()
        return context

class StudentProfileSstView(SstCheckMixin, DetailView):
    '''Function to show Student profile for SST'''
    model = Student
    template_name = 'school/sst/student_profile_sst.html'
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['supports'] = Support.objects.filter(
            student=self.object).select_related('sst')
        context['observations'] = Observation.objects.filter(
            student=self.object).select_related('sst')

        return context


class OccupationalTherapyView(SstCheckMixin, DetailView):
    '''Show occupational therapy for a sst team from a student profile'''
    model = OcupationalTherapy
    template_name = 'school/occup_therap_sst.html'
    login_url = 'login'


class SpeechTherapyView(SstCheckMixin, DetailView):
    '''Show speach therapy for SST team from a student profile'''
    model = SpeechTherapy
    template_name = "school/speech_therapy_sst.html"
    login_url = 'login'


class DownloadSampleUsers(StaffCheckMixin, View):

    def post(self, request, *args, **kwargs):
        if request.POST['sample'] == 'users':
            return create_sample_excel_users(request)

        elif request.POST['sample'] == 'students':
            return create_sample_excel_students(request)


class CustomPasswordChangeView(PasswordChangeView):
    '''Custom class to change password'''
    template_name = 'registration/custom_password_change_form.html'
    success_url = reverse_lazy("school:password_change_done_custom")


class CustomPasswordDoneView(PasswordChangeDoneView):
    '''Custom class to verify password changes'''
    template_name = 'registration/custom_password_change_done.html'


class CreateNewStream(TeacherCheckMixin, View):
    '''View to create new stream in responce to 
    post request from fetch (student profile page)
    '''

    def post(self, request):
        stream_data = json.load(request)
        # get datetime now
        now_date = datetime.now()
        # now_date_str = now_date.strftime("%d-%m-%Y"),
        review_date = now_date + timedelta(days=21)

        stream = Stream(
            name=stream_data['stream_name'],
            student=Student.objects.get(id=stream_data['stud_id']),
            teacher=request.user,
            date_start=now_date,
            date_review=review_date,
        )
        stream.save()
        data = {'stream': stream.id, }
        return JsonResponse(data, safe=False)
