import re
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import ObjectDoesNotExist

from .models import Consern, Intake, NotesPTS, Student, MyUser, Observation, Support
from .forms import MyUserForm, UploadExcelFileForm, ConsernForm, IntakeForm, SupportForm
from .utils import read_excel_with_students, calculate_age, sst_check, teacher_check, staff_check
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
            elif user.is_staff:
                return HttpResponseRedirect(reverse('school:staff_view'))
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
        notes = NotesPTS.objects.filter(student=student)
        concerns = Consern.objects.filter(student = student)
        observations = Observation.objects.filter(student=student)
        supports = Support.objects.filter(student=student)
        
        context = {
            'student': student,
            'age_years': age_years,
            'age_months': age_months,
            'notes': notes, 
            'concerns': concerns,
            'observations': observations,
            'supports': supports
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
                new_intake.concern = new_concern
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
    '''Function to show main page for SST'''
    if request.method == 'GET':
        concerns = Consern.objects.filter(refers = Consern.REFERRAL)
        # print(concerns.values())
        context = {
            'concerns': concerns
        }

        return render(request, 'school/sst.html', context)

@user_passes_test(sst_check)
def save_observation(request):
    '''Function to save observation from SST team
    via fetch api call'''
    if request.method == 'POST':
        observ_data = json.load(request)
        observation = Observation(
                                date = observ_data['obs_date'],
                                note = observ_data['obs_text'],
                                teacher = MyUser.objects.get(id=observ_data['teach_id']),
                                student = Student.objects.get(id=observ_data['stud_id']),
                                sst = request.user
                                )
        observation.save()
        data = {'status': 200}
        return JsonResponse(data, safe=False)

@user_passes_test(sst_check)
def support(request, **kwargs):
    if request.method == 'GET':
        student = Student.objects.get(id=kwargs['stud_id'])
        support_form = SupportForm()
        context = {
            'support_form':support_form,
            'student': student
            }
        return render(request, 'school/support.html', context)

@user_passes_test(sst_check)
def make_support_post(request):
    if request.method == "POST":
        support_form = SupportForm(request.POST)
        if support_form.is_valid():
            student = Student.objects.get(id=request.POST['stud_id'])
            teacher = MyUser.objects.get(id=request.POST['teach_id'])
            sst = request.user
            new_support = support_form.save(commit=False)
            new_support.student = student
            new_support.sst = sst
            new_support.teacher = teacher
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

@user_passes_test(sst_check)
def sst_view_intake(request):
    if request.method == 'POST':
        concern = Consern.objects.get(id = request.POST['concern_id'])
        concern_form = ConsernForm(instance=concern)
        for fieldname in concern_form.fields:
            concern_form.fields[fieldname].disabled = True

        intake_data = Intake.objects.get(concern=concern)
        intake_form = IntakeForm(instance=intake_data)
        for fieldname in intake_form.fields:
            intake_form.fields[fieldname].disabled = True

        student = Student.objects.get(stud_consern=concern)
        
        print(intake_data.sst_reasoning)
        print(student.first_name)
        context = {
            'cons_form': concern_form,
            'intake_form': intake_form,
            'student': student

        }
        return render(request, 'school/sst_intake.html', context)


@user_passes_test(teacher_check)
def update_concern(request):
    '''Function to update concern form and intake forms'''
    if request.method == 'GET':
        concern = Consern.objects.get(id =request.GET['concern_id'])
        concern_form = ConsernForm(instance=concern)
        
        try: 
            intake_form = IntakeForm(instance=concern.consern_intake)
            student = concern.student
            context = {
                    'concern_form': concern_form,
                    'intake_form': intake_form,
                    'student': student
                }
        # if concern doesn have an intake form 
        except ObjectDoesNotExist:
            context = {
                    'concern_form': concern_form,
                }
        return render(request, 'school/update_concern.html', context)

    if request.method == 'POST':
        print(request.POST)
        pass
    # save concerns updates 
    # TODO Teacher can update concern form 


# show supports note on teacher page 
# reply from teacher to a support