from django.shortcuts import get_object_or_404
from openpyxl import load_workbook
from .models import Student, MyUser

def read_excel_with_students(request_file):
    '''Function to read data from excel file uploaded from a user
    and save data to a database'''
    # print(request.user)
    print(request_file)
    wb = load_workbook(filename = request_file, data_only=True)
    sheet_ranges = wb.active

    sheet_ranges.max_column
    sheet_ranges.max_row

    stud_data = list(sheet_ranges.values)

    students_objects_list = []
    for row in stud_data[1:]:
        student = Student(
                school_id = row[0],
                first_name = row[1],
                middle_name = row[2],
                last_name = row[3],
                preferred_name = row[4], 
                date_of_birth = row[5], 
                birth_order_in_class = int(row[6]), 
                birth_order_in_family = int(row[7]), 
                gender = row[8],
                cur_grade = int(row[9]),
                grad_year = row[10],
                email = row[11],
                home_lang = row[12],
                date_join = row[13],
                entrygrades = row[14],
                teacher = get_teacher(row[15])
        )

        students_objects_list.append(student)

    new_sudents = Student.objects.bulk_create(students_objects_list, ignore_conflicts=True)

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
    


    # with open(filename, 'r') as destination:
    #     for chunk in filename.chunks():
    #         print(destination.read(chunk))
    # pass