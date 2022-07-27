from django.urls import path
from . import views

app_name = 'school'

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('teacher', views.teacher_view, name='teacher_view'),
    path('upload_students', views.upload_students, name='upload_students'),
    path('student_data_profile/<int:stud_id>', views.student_data_profile, name='student_data_profile'),
    path('make_consern/<int:stud_id>', views.make_consern, name='make_consern'),

    #API 
    path('save_note_from_PTC', views.save_note_from_PTC, name='save_note_from_PTC')

]