from django.urls import path
from django.contrib.auth import views as auth_view
from . import views

app_name = 'school'

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('teacher', views.teacher_view, name='teacher_view'),
    path('sst', views.sst_view, name='sst_view'),
    path('sst/support/<int:conc_id>', views.support, name='support'),
    path('sst/review/<int:pk>/', views.ShowReviewSST.as_view(), name='sst_read_review'),
    path('sst/intake/<int:pk>/', views.ShowIntakeSST.as_view(), name='sst_read_intake'),

    path('sst/student_profile/<int:pk>/',
         views.StudentProfileSstView.as_view(), name='student_profile'),
    path('sst/student_profile/<int:pk>/occupational_therapy',
         views.OccupationalTherapyView.as_view(), name='show_therapy_sst'),
    path('sst/student_profile/<int:pk>/speech_therapy',
         views.SpeechTherapyView.as_view(), name='show_speech_sst'),
    path('sst/student_profile/<int:pk>/support/',
         views.ReadSupportSstView.as_view(), name='read_full_support_text_sst'),
    path('sst/student_profile/<int:pk>/observation/',
         views.ShowObservationTextSstView.as_view(), name='read_full_observ_text_sst'),

    path('make_support_post/', views.make_support_post, name='make_support_post'),
    path('upload_students', views.upload_students, name='upload_students'),

    # Teacher
    path('student_data_profile/<int:stud_id>',
         views.student_data_profile, name='student_data_profile'),
    path('student_data_profile/<int:stud_id>/create_response/<int:supp_pk>/',
         views.CreateResponse.as_view(), name='create_response'),
    path('student_data_profile/<int:stud_id>/speech_therapy/<int:pk>/',
         views.ShowSpeechTherapy.as_view(), name='show_speech_ther'),
    path('student_data_profile/<int:stud_id>/occup_therapy/<int:pk>/',
         views.ShowOcupTherapy.as_view(), name='show_occup_ther'),
    path('student_data_profile/<int:stud_id>/show_support/<int:pk>/',
         views.ShowSupport.as_view(), name='read_full_support'),
    path('student_data_profile/<int:stud_id>/show_note/<int:pk>/',
         views.ShowNote.as_view(), name='show_note_text'),
    path('student_data_profile/<int:stud_id>/show_observation/<int:pk>/',
         views.ShowObservation.as_view(), name='show_observation'),
    path('student_data_profile/<int:stud_id>/new_read_screen/',
         views.ReadingScreenView.as_view(), name='new_read_screen'),
    path('student_data_profile/<int:stud_id>/show_read_screen/<int:pk>/',
         views.ShowReadScreen.as_view(), name='show_read_screen'),

    path('make_review/<int:stud_id>/<int:stream_id>', views.make_review, name='make_review'),
    path('make_review_post/', views.make_review_post, name='make_review_post'),
    path('read_review/<int:pk>/', views.ShowReviewTeacher.as_view(), name='read_review'),
    path('staff', views.staff_view, name='staff_view'),
    path('read_intake/<int:pk>', views.ShowIntakeTeacher.as_view(), name='read_intake'),

    # API
    path('save_note_from_PTC', views.save_note_from_PTC,
         name='save_note_from_PTC'),
    path('save_observation', views.save_observation, name='save_observation'),
    path('download_users', views.DownloadSampleUsers.as_view(),
         name='download_sample_users'),
    path('new_stream', views.CreateNewStream.as_view(), name='new_stream'),


    
    path('ocupational_therapy/<int:stud_id>',
         views.ocupational_therapy, name='ocupational_therapy'),
    path('ocupational_therapy_post', views.ocupational_therapy_post,
         name='ocupational_therapy_post'),
    path('speech_therapy/<int:stud_id>',
         views.speech_therapy, name='speech_therapy'),
    path('speech_therapy_post', views.speech_therapy_post,
         name='speech_therapy_post'),
    path('upload_users', views.upload_users, name='upload_users'),
    path('change-password/', views.CustomPasswordChangeView.as_view(), name='password_change'),
    path('change-password/done/', views.CustomPasswordDoneView.as_view(), name='password_change_done_custom')
    

]
