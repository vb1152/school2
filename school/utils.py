from django.contrib.auth.mixins import UserPassesTestMixin

from openpyxl import load_workbook
from .models import Student, MyUser, UsersData
from .forms import UploadExcelFileForm


def read_excel_with_students(request_file):
    '''Function to read data from excel file uploaded from a user
    and save data to a database'''
    wb = load_workbook(filename=request_file, data_only=True)
    sheet_ranges = wb.active
    sheet_ranges.max_column
    sheet_ranges.max_row
    stud_data = list(sheet_ranges.values)
    students_objects_list = []

    for row in stud_data[1:]:

        if Student.objects.filter(first_name=row[1], last_name=row[3], date_of_birth=row[5]).exists():
            continue
        else:
            student = Student(
                school_id=row[0],
                first_name=row[1],
                middle_name=row[2],
                last_name=row[3],
                preferred_name=row[4],
                date_of_birth=row[5],
                birth_order_in_class=int(row[6]),
                birth_order_in_family=int(row[7]),
                # add gender to db or empty value if not Male or Femail are actual data in excel.
                gender='M' if row[8] == 'Male' else (
                    'F' if row[8] == 'Female' else 'smt'),
                cur_grade=int(row[9]),
                grad_year=row[10],
                email=row[11],
                home_lang=row[12],
                date_join=row[13],
                entrygrades=row[14],
                teacher=get_teacher(row[15])
            )

        students_objects_list.append(student)

    new_sudents = Student.objects.bulk_create(
        students_objects_list)  # , ignore_conflicts=True)

    return (len(new_sudents), 'Success!')


def read_excel_save_users(request):
    form = UploadExcelFileForm(request.POST, request.FILES)
    if form.is_valid():
        request_file = request.FILES['file']
        wb = load_workbook(filename=request_file, data_only=True)
        sheet_ranges = wb.active
        sheet_ranges.max_column
        sheet_ranges.max_row
        user_data = list(sheet_ranges.values)
        user_counter = 0
        for row in user_data[1:]:
            if MyUser.objects.filter(username=row[1]).exists():
                continue
            else:
                user = MyUser.objects.create_user(
                    username=row[1],
                    password=row[1],
                    first_name=row[3],
                    last_name=row[4],
                    email=row[6])

                if row[5] == 'teacher':
                    user.is_teacher = True
                elif row[5] == 'sst':
                    user.is_sst = True
                elif row[5] == 'counselor':
                    user.is_conselor = True
                user.save()

                user_data = UsersData.objects.create(
                    user=user,
                    person_id=row[0],
                    grades=row[2])
                user_data.save()
                user_counter += 1
        return user_counter


def get_teacher(teacher_data) -> object:
    '''Find teacher instanse in data base. 
    If not - return None
    -----------
    Return MyUser object (teacher == True)
    '''
    firstname, lastname = teacher_data.split()
    try:
        teach_inst = MyUser.objects.get(
            first_name=firstname,
            last_name=lastname,
            is_teacher=True)
        return teach_inst
    except MyUser.DoesNotExist:
        return None


def calculate_age(date_of_birth):
    '''Calculate students age form date of birth'''
    from datetime import datetime
    from dateutil import relativedelta

    now = datetime.now()
    # convert string to date object
    start_date = datetime.strptime(date_of_birth, "%Y-%m-%d")
    # Get the relativedelta between two dates
    delta = relativedelta.relativedelta(now, start_date)
    return (delta.years, delta.months)


def teacher_check(user):
    '''Check if user is a teacher for user_passes_test decorator'''
    return user.is_teacher


def sst_check(user):
    '''Check if user is a sst for user_passes_test decorator'''
    return user.is_sst


def staff_check(user):
    '''Check if user is a sst for user_passes_test decorator'''
    return user.is_staff


class TeacherCheckMixin(UserPassesTestMixin):
    '''Check if user us a teacher'''

    def test_func(self):
        return self.request.user.is_teacher


class SstCheckMixin(UserPassesTestMixin):
    '''Check if user is a sst for user_passes_test decorator'''

    def test_func(self):
        return self.request.user.is_sst

        # http://127.0.0.1:8000/sst/student_profile/2/speech_therapy
