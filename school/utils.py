from django.shortcuts import get_object_or_404
from openpyxl import load_workbook
from .models import Student, MyUser

def read_excel_with_students(request_file):
    '''Function to read data from excel file uploaded from a user
    and save data to a database'''
    print(request_file)
    wb = load_workbook(filename = request_file, data_only=True)
    sheet_ranges = wb.active

    sheet_ranges.max_column
    sheet_ranges.max_row

    stud_data = list(sheet_ranges.values)

    students_objects_list = []

    print(stud_data[1:])
    
    for row in stud_data[1:]:
        
        if Student.objects.filter(first_name = row[1], last_name = row[3], date_of_birth = row[5]).exists():
            continue
        else:
            student = Student(
                    school_id = row[0],
                    first_name = row[1],
                    middle_name = row[2],
                    last_name = row[3],
                    preferred_name = row[4], 
                    date_of_birth = row[5], 
                    birth_order_in_class = int(row[6]), 
                    birth_order_in_family = int(row[7]), 
                    # add gender to db or empty value if not Male or Femail are actual data in excel. 
                    gender = 'M' if row[8] == 'Male' else ('F' if row[8] == 'Female' else 'smt'),
                    cur_grade = int(row[9]),
                    grad_year = row[10],
                    email = row[11],
                    home_lang = row[12],
                    date_join = row[13],
                    entrygrades = row[14],
                    teacher = get_teacher(row[15])
            )

        students_objects_list.append(student)

    new_sudents = Student.objects.bulk_create(students_objects_list)#, ignore_conflicts=True)

    return (len(new_sudents), 'Success!')


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