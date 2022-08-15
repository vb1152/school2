from django.test import TestCase, SimpleTestCase, Client, RequestFactory
from django.contrib.auth.models import AnonymousUser, User
from .models import MyUser
from django.contrib.auth import get_user_model
from django.urls import reverse, resolve

from .models import MyUser
from .views import (index, login_view, upload_users,
                    teacher_view, sst_view, support,
                    sst_view_intake, make_support_post,
                    upload_students, student_data_profile,
                    make_consern, make_consern_post, staff_view,
                    save_note_from_PTC, save_observation,
                    update_concern, ocupational_therapy,
                    ocupational_therapy_post, speech_therapy,
                    speech_therapy_post, upload_users,

                    StudentProfileSstView, OccupationalTherapyView,
                    SpeechTherapyView, ShowConcernSST, ReadSupportSstView,
                    ShowObservationTextSstView, CreateResponse,
                    ShowSpeechTherapy, ShowOcupTherapy, ShowSupport,
                    ShowNote, ShowObservation, ReadingScreenView,
                    ShowReadScreen,
                    )
# from school_system.school import views

# Create your tests here.


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
        self.assertEquals(resolve(url).func, teacher_view)

    def test_sst_url_resolves(self):
        url = reverse('school:sst_view')
        self.assertEquals(resolve(url).func, sst_view)

    def test_sst_support_url_resolves(self):
        url = reverse('school:support', args=[1])
        self.assertEquals(resolve(url).func, support)

    def test_sst_intake_url_resolve(self):
        url = reverse('school:sst_view_intake')
        self.assertEquals(resolve(url).func, sst_view_intake)

    def test_sst_student_profile_url_resolve(self):
        url = reverse('school:student_profile', args=[1])
        self.assertEquals(resolve(url).func.view_class,
                          StudentProfileSstView)

    def test_sst_show_therapy_url_resolve(self):
        url = reverse('school:show_therapy_sst', args=[1])
        self.assertEquals(resolve(url).func.view_class,
                          OccupationalTherapyView)

    def test_sst_show_speech_url_resolve(self):
        url = reverse('school:show_speech_sst', args=[1])
        self.assertEquals(resolve(url).func.view_class,
                          SpeechTherapyView)

    def test_sst_show_concern_url_resolve(self):
        url = reverse('school:show_concern_sst', args=[1])
        self.assertEquals(resolve(url).func.view_class,
                          ShowConcernSST)

    def test_sst_read_full_support_url_resolve(self):
        url = reverse('school:read_full_support_text_sst', args=[1])
        self.assertEquals(resolve(url).func.view_class,
                          ReadSupportSstView)

    def test_sst_read_observat_url_resolve(self):
        url = reverse('school:read_full_observ_text_sst', args=[1])
        self.assertEquals(resolve(url).func.view_class,
                          ShowObservationTextSstView)

    def test_make_support_url_resolve(self):
        url = reverse('school:make_support_post')
        self.assertEquals(resolve(url).func, make_support_post)

    def test_uload_students_url_resolve(self):
        url = reverse('school:upload_students')
        self.assertEquals(resolve(url).func, upload_students)

    def test_student_profile_teacher_url_resolve(self):
        url = reverse('school:student_data_profile', args=[1])
        self.assertEquals(resolve(url).func, student_data_profile)

    def test_create_responce_teacher_url_resolve(self):
        url = reverse('school:create_response', args=[1, 2])
        self.assertEquals(resolve(url).func.view_class, CreateResponse)

    def test_show_seech_therap_teacher_url_resolve(self):
        url = reverse('school:show_speech_ther', args=[1, 2])
        self.assertEquals(resolve(url).func.view_class,
                          ShowSpeechTherapy)

    def test_show_ocup_therapy_teacher_url_resolve(self):
        url = reverse('school:show_occup_ther', args=[1, 2])
        self.assertEquals(resolve(url).func.view_class,
                          ShowOcupTherapy)

    def test_show_support_url_resolve(self):
        url = reverse('school:read_full_support', args=[1, 2])
        self.assertEquals(resolve(url).func.view_class,
                          ShowSupport)

    def test_show_note_url_resolve(self):
        url = reverse('school:show_note_text', args=[1, 2])
        self.assertEquals(resolve(url).func.view_class, ShowNote)

    def test_show_observations_url_resolve(self):
        url = reverse('school:show_observation', args=[1, 2])
        self.assertEquals(resolve(url).func.view_class, ShowObservation)

    def test_read_screen_url_resolve(self):
        url = reverse('school:new_read_screen', args=[1])
        self.assertEquals(resolve(url).func.view_class, ReadingScreenView)

    def test_show_readscreen_url_resolve(self):
        url = reverse('school:show_read_screen', args=[1, 2])
        self.assertEquals(resolve(url).func.view_class, ShowReadScreen)

    def test_make_consern_url_resolve(self):
        url = reverse('school:make_consern', args=[1])
        self.assertEquals(resolve(url).func, make_consern)

    def test_make_consern_post_url_resolve(self):
        url = reverse('school:make_consern_post')
        self.assertEquals(resolve(url).func, make_consern_post)

    def test_staff_view_url_resolve(self):
        url = reverse('school:staff_view')
        self.assertEquals(resolve(url).func, staff_view)

    def test_save_note_url_resolve(self):
        url = reverse('school:save_note_from_PTC')
        self.assertEquals(resolve(url).func, save_note_from_PTC)

    def test_save_observations_url_resolve(self):
        url = reverse('school:save_observation')
        self.assertEquals(resolve(url).func, save_observation)

    def test_update_concern_url_resolve(self):
        url = reverse('school:update_concern')
        self.assertEquals(resolve(url).func, update_concern)

    def test_ocupationl_ther_url_resove(self):
        url = reverse('school:ocupational_therapy', args=[1])
        self.assertEquals(resolve(url).func, ocupational_therapy)

    # kwargs={'stud_id': 1} # stud_id
    def test_ocupational_therapy_post(self):
        url = reverse('school:ocupational_therapy_post')
        self.assertEquals(resolve(url).func, ocupational_therapy_post)

    def test_speech_therap_url_resolve(self):
        url = reverse('school:speech_therapy', args=[1])
        self.assertEquals(resolve(url).func, speech_therapy)

    def test_speech_therapy_post_url_resolve(self):
        url = reverse('school:speech_therapy_post')
        self.assertEquals(resolve(url).func, speech_therapy_post)

    def test_upload_users_post_url_resolve(self):
        url = reverse('school:upload_users')
        self.assertEqual(resolve(url).func, upload_users)


class MyTest(TestCase):

    def setUp(self) -> None:
        self.client = Client()
        self.factory = RequestFactory()
        self.teacher_user = MyUser.objects.create_user(
            username='Amy_Doe', email='a@a.com', password='1', is_teacher=True)
        self.sst_user = MyUser.objects.create_user(
            username='Bar_SST', email='sst@sst.com', password='1', is_sst=True)

    # required registered user
    def test_teacher_url_exists(self):
        logged_in = self.client.login(
            username=self.teacher_user.username, password='1')
        resp = self.client.get('/teacher')
        self.assertEqual(resp.status_code, 200)

     # required registered user
    def test_teacher_view_use_template(self):
        logged_in = self.client.login(
            username=self.teacher_user.username, password='1')
        resp = self.client.get(reverse('school:teacher_view'))
        self.assertTemplateUsed(resp, 'school/teacher.html')

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
