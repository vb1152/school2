from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Student
from .forms import MyUserForm, UploadExcelFileForm
from .utils import read_excel_with_students, calculate_age


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
        
        print(student.date_of_birth)#, print(type(student.date_of_birth)))
        age_years, age_months = calculate_age(str(student.date_of_birth))

        context = {
            'student': student,
            'age_years': age_years,
            'age_months': age_months
        }
        return render(request, 'school/student_profile.html', context)