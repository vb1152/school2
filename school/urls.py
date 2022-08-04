from django.urls import path
from . import views

app_name = 'school'

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('teacher', views.teacher_view, name='teacher_view'),
    path('sst', views.sst_view, name='sst_view'),
    path('sst/support/<int:stud_id>', views.support, name='support'),
    path('sst/intake/', views.sst_view_intake, name='sst_view_intake'),
    path('make_support_post/', views.make_support_post, name='make_support_post'),


    path('upload_students', views.upload_students, name='upload_students'),
    path('student_data_profile/<int:stud_id>', views.student_data_profile, name='student_data_profile'),
    path('make_consern/<int:stud_id>', views.make_consern, name='make_consern'),
    path('make_consern_post', views.make_consern_post, name='make_consern_post'),
    path('staff', views.staff_view, name='staff_view'),

    #API 
    path('save_note_from_PTC', views.save_note_from_PTC, name='save_note_from_PTC'),
    path('save_observation', views.save_observation, name='save_observation'),

    path('update_concern/', views.update_concern, name='update_concern'), 
    path('ocupational_therapy/<int:stud_id>', views.ocupational_therapy, name='ocupational_therapy'), 
    path('ocupational_therapy_post', views.ocupational_therapy_post, name = 'ocupational_therapy_post'),
    path('speech_therapy/<int:stud_id>', views.speech_therapy, name='speech_therapy'),
    path('speech_therapy_post', views.speech_therapy_post, name='speech_therapy_post')
]