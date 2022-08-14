from django.test import TestCase, SimpleTestCase, Client
from django.urls import reverse, resolve
from .views import (index, login_view, upload_users,
                    teacher_view, sst_view, support,
                    sst_view_intake, make_support_post,
                    upload_students, student_data_profile,
                    StudentProfileSstView, OccupationalTherapyView,
                    SpeechTherapyView, ShowConcernSST, ReadSupportSstView,
                    ShowObservationTextSstView, CreateResponse,
                    ShowSpeechTherapy, ShowOcupTherapy, ShowSupport
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

    # required registered user
    # def test_teacher_url_exists(self):
    #     resp = self.client.get('/teacher')
    #     self.assertEqual(resp.status_code, 200)

    def test_teacher_url_resolves(self):
        url = reverse('school:teacher_view')
        self.assertEquals(resolve(url).func, teacher_view)

    # # required registered user
    # def test_teacher_view_use_template(self):
    #     resp = self.client.get(reverse('school:teacher_view'))
    #     self.assertTemplateUsed(resp, 'school/teacher.html')

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

# class TestViews(TestCase):
#     def setUp(self) -> None:
#         self.client = Client()
