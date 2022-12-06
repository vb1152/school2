import json

from django.test import TestCase, SimpleTestCase, Client, RequestFactory
from django.contrib.auth.models import AnonymousUser, User
from django.contrib.auth import get_user_model
from django.urls import reverse, resolve
from datetime import date


from .models import MyUser, Student, NotesPTS
from .views import (index, login_view, upload_users,
                    teacher_view, sst_view,
                    make_support_post,
                    upload_students, student_data_profile,
                    staff_view,
                    save_note_from_PTC, save_observation,
                    ocupational_therapy,
                    ocupational_therapy_post, speech_therapy,
                    speech_therapy_post, upload_users,

                    StudentProfileSstView, OccupationalTherapyView,
                    SpeechTherapyView, ReadSupportSstView,
                    ShowObservationTextSstView, CreateResponse,
                    ShowSpeechTherapy, ShowOcupTherapy, ShowSupport,
                    ShowNote, ShowObservation, ReadingScreenView,
                    ShowReadScreen, DownloadSampleUsers, CreateNewStream,
                    ReadScreenSSTView
                    )


class TestUrls(SimpleTestCase):
    def test_view_url_exists_at_proper_location(self):
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)

    def test_view_url_by_name(self):
        resp = self.client.get(reverse('school:index'))
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('school:index'))
        self.assertTemplateUsed(resp, 'school/index.html')

    def test_check_view_name(self):
        resp = self.client.get('/')
        self.assertEqual(resp.resolver_match.func, index)

    def test_login_url_exists(self):
        resp = self.client.get('/login')
        self.assertEqual(resp.status_code, 200)

    def test_view_login_url_by_name(self):
        # test reverse url name
        resp = self.client.get(reverse('school:login'))
        self.assertEqual(resp.status_code, 200)

    def test_view_login_uses_correct_template(self):
        # test the correct template
        resp = self.client.get(reverse('school:login'))
        self.assertTemplateUsed(resp, 'school/login.html')

    def test_check_view_login_name(self):
        # test the correct view name
        resp = self.client.get('/login')
        self.assertEqual(resp.resolver_match.func, login_view)

    def test_teacher_url_resolves(self):
        url = reverse('school:teacher_view')
        self.assertEqual(resolve(url).func, teacher_view)

    def test_sst_url_resolves(self):
        url = reverse('school:sst_view')
        self.assertEqual(resolve(url).func, sst_view)

    def test_sst_student_profile_url_resolve(self):
        url = reverse('school:student_profile', args=[1])
        self.assertEqual(resolve(url).func.view_class,
                         StudentProfileSstView)

    def test_sst_show_therapy_url_resolve(self):
        url = reverse('school:show_therapy_sst', args=[1, 2])
        self.assertEqual(resolve(url).func.view_class,
                         OccupationalTherapyView)

    def test_sst_show_speech_url_resolve(self):
        url = reverse('school:show_speech_sst', args=[1, 2])
        self.assertEqual(resolve(url).func.view_class,
                         SpeechTherapyView)

    def test_sst_read_full_support_url_resolve(self):
        url = reverse('school:read_full_support_text_sst', args=[1, 2])
        self.assertEqual(resolve(url).func.view_class,
                         ReadSupportSstView)

    def test_sst_read_observat_url_resolve(self):
        url = reverse('school:read_full_observ_text_sst', args=[1])
        self.assertEqual(resolve(url).func.view_class,
                         ShowObservationTextSstView)

    def test_make_support_url_resolve(self):
        url = reverse('school:make_support_post')
        self.assertEqual(resolve(url).func, make_support_post)

    def test_uload_students_url_resolve(self):
        url = reverse('school:upload_students')
        self.assertEqual(resolve(url).func, upload_students)

    def test_student_profile_teacher_url_resolve(self):
        url = reverse('school:student_data_profile', args=[1])
        self.assertEqual(resolve(url).func, student_data_profile)

    def test_create_responce_teacher_url_resolve(self):
        url = reverse('school:create_response', args=[1, 2])
        self.assertEqual(resolve(url).func.view_class, CreateResponse)

    def test_show_seech_therap_teacher_url_resolve(self):
        url = reverse('school:show_speech_ther', args=[1, 2])
        self.assertEqual(resolve(url).func.view_class,
                         ShowSpeechTherapy)

    def test_show_ocup_therapy_teacher_url_resolve(self):
        url = reverse('school:show_occup_ther', args=[1, 2])
        self.assertEqual(resolve(url).func.view_class,
                         ShowOcupTherapy)

    def test_show_support_url_resolve(self):
        url = reverse('school:read_full_support', args=[1, 2])
        self.assertEqual(resolve(url).func.view_class,
                         ShowSupport)

    def test_show_note_url_resolve(self):
        url = reverse('school:show_note_text', args=[1, 2])
        self.assertEqual(resolve(url).func.view_class, ShowNote)

    def test_show_observations_url_resolve(self):
        url = reverse('school:show_observation', args=[1, 2])
        self.assertEqual(resolve(url).func.view_class, ShowObservation)

    def test_read_screen_url_resolve(self):
        url = reverse('school:new_read_screen', args=[1])
        self.assertEqual(resolve(url).func.view_class, ReadingScreenView)

    def test_show_readscreen_url_resolve(self):
        url = reverse('school:show_read_screen', args=[1, 2])
        self.assertEqual(resolve(url).func.view_class, ShowReadScreen)

    def test_staff_view_url_resolve(self):
        url = reverse('school:staff_view')
        self.assertEqual(resolve(url).func, staff_view)

    def test_save_note_url_resolve(self):
        url = reverse('school:save_note_from_PTC')
        self.assertEqual(resolve(url).func, save_note_from_PTC)

    def test_save_observations_url_resolve(self):
        url = reverse('school:save_observation')
        self.assertEqual(resolve(url).func, save_observation)

    def test_ocupationl_ther_url_resove(self):
        url = reverse('school:ocupational_therapy', args=[1])
        self.assertEqual(resolve(url).func, ocupational_therapy)

    def test_ocupational_therapy_post(self):
        url = reverse('school:ocupational_therapy_post')
        self.assertEqual(resolve(url).func, ocupational_therapy_post)

    def test_speech_therap_url_resolve(self):
        url = reverse('school:speech_therapy', args=[1])
        self.assertEqual(resolve(url).func, speech_therapy)

    def test_speech_therapy_post_url_resolve(self):
        url = reverse('school:speech_therapy_post')
        self.assertEqual(resolve(url).func, speech_therapy_post)

    def test_upload_users_post_url_resolve(self):
        url = reverse('school:upload_users')
        self.assertEqual(resolve(url).func, upload_users)

    def test_download_sample_users_url_resolve(self):
        url = reverse('school:download_sample_users')
        self.assertEqual(resolve(url).func.view_class, DownloadSampleUsers)

    def test_new_stream_url_resolve(self):
        url = reverse('school:new_stream')
        self.assertEqual(resolve(url).func.view_class, CreateNewStream)

class MyTest(TestCase):

    def setUp(self) -> None:
        self.client = Client()
        self.factory = RequestFactory()
        MyUser = get_user_model()

        self.teacher_user = MyUser.objects.create_user(
            username='Amy_Doe', email='a@a.com', password='1', is_teacher=True)
        self.sst_user = MyUser.objects.create_user(
            username='Bar_SST', email='sst@sst.com', password='1', is_sst=True)

        self.staf_user = MyUser.objects.create_user(
            username='Staff', email='staff@staff.com', password='1',
            is_staff=True)

        self.student = Student.objects.create(
            school_id='53',
            first_name='Alex',
            middle_name=None,
            last_name='Max',
            preferred_name='Alex',
            date_of_birth=date(2019, 12, 4),
            birth_order_in_class=2,
            birth_order_in_family=3,
            gender='Male',
            cur_grade=5,
            grad_year='2023',
            email=None,
            home_lang='English',
            date_join=date(2021, 9, 1),
            entrygrades=5,
            teacher=self.teacher_user
        )

        self.note_pts = NotesPTS.objects.create(
            student=self.student,
            date=date.today(),
            note='Some note from PTS'
        )

        
    def test_student_string_representation(self):
        student = Student(first_name='Name', last_name='Last')
        self.assertEqual(str(student), student.first_name
                         + ' ' + student.last_name)

    def test_notepts_string_representation(self):
        note = NotesPTS(date=date.today().strftime("%d/%m/%y"))
        self.assertEqual(str(note), note.date)

    def test_create_users(self):
        self.assertEqual(self.teacher_user.username, 'Amy_Doe')
        self.assertEqual(self.teacher_user.email, 'a@a.com')
        self.assertTrue(self.teacher_user.is_teacher)
        self.assertFalse(self.teacher_user.is_staff)
        self.assertFalse(self.teacher_user.is_sst)

        self.assertEqual(self.sst_user.username, 'Bar_SST')
        self.assertEqual(self.sst_user.email, 'sst@sst.com')
        self.assertTrue(self.sst_user.is_sst)
        self.assertFalse(self.sst_user.is_teacher)

        self.assertEqual(self.staf_user.username, 'Staff')
        self.assertEqual(self.staf_user.email, 'staff@staff.com')
        self.assertTrue(self.staf_user.is_staff)
        self.assertFalse(self.staf_user.is_superuser)

     # required registered user
    def test_sst_url_exists(self):
        logged_in = self.client.login(
            username=self.sst_user.username, password='1')
        resp = self.client.get('/sst')
        self.assertEqual(resp.status_code, 200)

    def test_sst_url_use_template(self):
        logged_in = self.client.login(
            username=self.sst_user.username, password='1')
        resp = self.client.get(reverse('school:sst_view'))
        self.assertTemplateUsed(resp, 'school/sst.html')

    def test_change_password_url_exists_at_proper_location(self):
        logged_in = self.client.login(
            username=self.teacher_user.username, password='1')
        resp = self.client.get('/change-password/')
        self.assertEqual(resp.status_code, 200)

    def test_change_passw_use_propper_template(self):
        logged_in = self.client.login(
            username=self.staf_user.username, password='1')
        resp = self.client.get(reverse('school:password_change'))
        self.assertTemplateUsed(resp, 'registration/custom_password_change_form.html')
        self.assertContains(resp, "Password Change")

    def test_password_change_done_url_exists(self):
        logged_in = self.client.login(
            username=self.staf_user.username, password='1')
        resp = self.client.get('/change-password/done/')
        self.assertEqual(resp.status_code, 200)

    def test_change_password_done_use_proper_template(self):
        logged_in = self.client.login(
            username=self.staf_user.username, password='1')
        resp = self.client.get(reverse('school:password_change_done_custom'))
        self.assertTemplateUsed(resp, 'registration/custom_password_change_done.html')

class TestTeacherPages(TestCase):
    
    def setUp(self) -> None:
        self.client = Client()
        self.factory = RequestFactory()
        MyUser = get_user_model()

        self.teacher_user = MyUser.objects.create_user(
            username='Amy_Doe', email='a@a.com', password='1', is_teacher=True)
        
        self.teacher_user2 = MyUser.objects.create_user(
            username='Jamie_Doe', email='b@b.com', password='1', is_teacher=True)

        self.student = Student.objects.create(
            school_id='53',
            first_name='Alex',
            middle_name=None,
            last_name='Max',
            preferred_name='Alex',
            date_of_birth=date(2019, 12, 4),
            birth_order_in_class=2,
            birth_order_in_family=3,
            gender='Male',
            cur_grade=5,
            grad_year='2023',
            email=None,
            home_lang='English',
            date_join=date(2021, 9, 1),
            entrygrades=5,
            teacher=self.teacher_user
        )
        # another student with another teacher
        self.student = Student.objects.create(
            school_id='6',
            first_name='Mart',
            middle_name=None,
            last_name='Mat',
            preferred_name='Bar',
            date_of_birth=date(2019, 12, 4),
            birth_order_in_class=2,
            birth_order_in_family=3,
            gender='Male',
            cur_grade=5,
            grad_year='2023',
            email=None,
            home_lang='English',
            date_join=date(2021, 9, 1),
            entrygrades=5,
            teacher=self.teacher_user2
        )

        logged_in = self.client.login(
            username=self.teacher_user.username, password='1')

    def test_teacher_url_exists(self):
        resp = self.client.get('/teacher')
        self.assertEqual(resp.status_code, 200)

    def test_teacher_view_use_template(self):
        resp = self.client.get(reverse('school:teacher_view'))
        self.assertTemplateUsed(resp, 'school/teacher.html')
        self.assertContains(resp, "All students")
        # teacher page should contain links to teacher's students
        self.assertContains(resp, 'href="/student_data_profile/1"')
        self.assertNotContains(resp, 'href="/student_data_profile/2"')

    def test_student_profile_url_exists(self):
        resp = self.client.get('/student_data_profile/1')
        self.assertEqual(resp.status_code, 200)

    def test_new_stream_created_post(self):
        '''Test checks for:
        - accept post requests with data for a
            new stream
        - checks if stream is created and responce 
            with new stream data is returned. 
        '''
        stream_data = {
            "stream_name": "Care and Therapeutic",
            "stud_id": 1,
        }
        resp = self.client.post('/new_stream', 
                                json.dumps(stream_data),
                                content_type="application/json")
        self.assertEqual(resp.status_code, 200)
        self.assertJSONEqual(str(resp.content, encoding='utf8'), 
                            {'stream': 1, })

class TestStaffPages(TestCase):
    '''Test case for a staff user'''
    def setUp(self) -> None:
        self.client = Client()
        self.factory = RequestFactory()
        MyUser = get_user_model()

        self.staf_user = MyUser.objects.create_user(
            username='Staff', email='staff@staff.com', password='1',
            is_staff=True)
            
        logged_in = self.client.login(
            username=self.staf_user.username, password='1')

    def test_staff_url_exists(self):
        resp = self.client.get('/staff')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'school/staff.html')

    def test_staff_view_post_download_users_request(self):
        '''Test for downloading sample file wit users.'''
        resp = self.client.post('/download_users', {'sample': 'users'})
        self.assertEqual(resp.get('Content-Disposition'),
                        "attachment; filename=Sample_users.xlsx")

    def test_staff_view_post_download_students_request(self):
        '''Test for downloading sample file with students'''
        resp = self.client.post('/download_users', {'sample': 'students'})
        self.assertEqual(resp.get('Content-Disposition'), 
                        'attachment; filename=Sample_students.xlsx')

class TestSSTpages(TestCase):
    '''Test case for a SST user'''
    def setUp(self) -> None:
        self.client = Client()
        self.factory = RequestFactory()
        MyUser = get_user_model()

        self.sst_user = MyUser.objects.create_user(
            username='Bar_SST', email='sst@sst.com', password='1', is_sst=True)

        self.teacher_user = MyUser.objects.create_user(
            username='Amy_Doe', email='a@a.com', password='1', is_teacher=True)

        self.student = Student.objects.create(
            school_id='1',
            first_name='Alan',
            middle_name=None,
            last_name='Max',
            preferred_name='Alan',
            date_of_birth=date(2000, 10, 5),
            birth_order_in_class=1,
            birth_order_in_family=1,
            gender='Male',
            cur_grade=8,
            grad_year='2025',
            email='alan@gmail.com',
            home_lang='English',
            date_join=date(2021, 11, 11),
            entrygrades=10,
            teacher=self.teacher_user
        )

        logged_in = self.client.login(
            username=self.sst_user.username, password='1')
    
    def test_read_screen_sst_url_resolve(self):
        url = reverse('school:show_readscreen_sst', args=[1, 2])
        self.assertEqual(resolve(url).func.view_class, ReadScreenSSTView)
        