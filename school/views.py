from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test

from .models import Consern, Intake, NotesPTS, Student, MyUser
from .forms import MyUserForm, UploadExcelFileForm, ConsernForm, IntakeForm
from .utils import read_excel_with_students, calculate_age, sst_check, teacher_check
import json


# Create your views here.
def index(request):
    '''Index function.'''
    return render(request, 'school/index.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        # check authentication
        if user is not None:
            login(request, user)
            if user.is_teacher == True: #redirect to a teacher page
                return HttpResponseRedirect(reverse('school:teacher_view'))
            elif user.is_sst == True:
                return HttpResponseRedirect(reverse('school:sst_view'))
            else:
                return HttpResponseRedirect(reverse('school:index'))
        
        else:
            messages.error(request, 'Wrong username and/or password')
            # return render(request, 'school/login.html')
            return HttpResponseRedirect(reverse('school:login'))

    else:
        user_form = MyUserForm()
        context = {
            'form': user_form
        }
        return render(request, 'school/login.html', context)

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('school:index'))

@login_required
@user_passes_test(teacher_check)
def teacher_view(request):
    excel_form = UploadExcelFileForm()
    # get list of students for one teacher
    students = Student.objects.filter(teacher = request.user)
    context = {
        'file_form': excel_form, 
        'students': students
    }
    return render(request, 'school/teacher.html', context)

@login_required
def upload_students(request):
    '''Save student to the data base '''
    if request.method == 'POST':
        form = UploadExcelFileForm(request.POST, request.FILES)
        if form.is_valid():
            print(request.user)
            result, message = read_excel_with_students(request.FILES['file'])
            messages.success(request, f'Saved {result} students profiles!')
            return HttpResponseRedirect(reverse('school:teacher_view'))
        else:
            messages.error(request, 'Something wrong')
            return HttpResponseRedirect(reverse('school:teacher_view'))

@login_required
def student_data_profile(request, **kwargs):
    if request.method == 'GET':
        student = get_object_or_404(Student, id=kwargs['stud_id'])
        age_years, age_months = calculate_age(str(student.date_of_birth))
        notes = NotesPTS.objects.filter(student=student)
        concerns = Consern.objects.filter(student = student)
        
        context = {
            'student': student,
            'age_years': age_years,
            'age_months': age_months,
            'notes': notes, 
            'concerns': concerns
        }
        return render(request, 'school/student_profile.html', context)

@login_required
@user_passes_test(teacher_check)
def save_note_from_PTC(request):
    if request.method == 'POST':
        note = json.load(request)
        student = Student.objects.get(id=note['stud_id'])
        note_inst = NotesPTS(student = student, date=note['note_date'], note=note['note_text'] )
        note_inst.save()
        # {'note_date': '2022-07-26', 'note_text': 'ads', 'stud_id': '5'}

        all_notes = NotesPTS.objects.filter(student=student).values()
        data = {'notes': list(all_notes),}
        return JsonResponse(data, safe=False)

@login_required
@user_passes_test(teacher_check)
def make_consern(request, **kwargs):
    if request.method == 'GET':
        
        student = Student.objects.get(id=kwargs['stud_id'])
        cons_form = ConsernForm()
        intake_form = IntakeForm()
        context = {
            'student': student,
            'cons_form': cons_form, 
            'intake_form': intake_form
        }
        return render(request, 'school/consern.html', context)

@login_required
@user_passes_test(teacher_check)
def make_consern_post(request):
    '''Function to save concern and intake forms to database.'''
    if request.method == 'POST':

        cons_form = ConsernForm(request.POST)
        intake_form = IntakeForm(request.POST)

        student = Student.objects.get(id=request.POST['stud_id'])
        teacher = MyUser.objects.get(id=request.user.id)

        if cons_form.is_valid():
            new_concern = cons_form.save(commit=False)
            new_concern.student = student
            new_concern.teacher = teacher
            new_concern.save()
            
            if intake_form.is_valid() and 'timeline' in request.POST and 'sst_reasoning' in request.POST:
                
                new_intake = intake_form.save(commit=False)
                new_intake.student = student
                new_intake.teacher = teacher
                new_intake.consern = new_concern
                new_intake.save()

                messages.success(request, 'Thank you! Concern and Intake data is saved!')
                return HttpResponseRedirect(reverse('school:student_data_profile', args=[student.id]))
            
            messages.success(request, 'Thank you! Concern is saved!')
            return HttpResponseRedirect(reverse('school:student_data_profile', args=[student.id]))
        
        messages.error(request, 'Some error. Concern is not saved.')
        return HttpResponseRedirect(reverse('school:student_data_profile', args=[request.POST['stud_id']]))
            
# @login_required
@user_passes_test(sst_check)
def sst_view(request):
    if request.method == 'GET':
        concerns = Consern.objects.filter(refers = Consern.REFERRAL)
        print(concerns.values())
        context = {
            'concerns': concerns
        }

        return render(request, 'school/sst.html', context)

@user_passes_test(sst_check)
def save_observation(request):
    if request.method == 'POST':
        print(request.POST)
        pass


# save observation note from SST 
# show observation note on teacher page 
# save support from SST 
# show supports note on teacher page 

# reply from teacher to a support