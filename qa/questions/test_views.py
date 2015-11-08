from django.test import TestCase
import json

from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

# from .views import QuestionDetailView
from .models import Question


class QuestionViewsTest(TestCase):

    def setUp(self):
        self.user_password = "password"
        self.another_username = 'john1'
        self.user = User.objects.create_user(
            username="John", email="john@dou.com", password=self.user_password)
        User.objects.create_user(
            username=self.another_username, password=self.user_password)
        self.question = Question.objects.create(
            title="Are you allright?",
            owner=self.user,
        )
        self.answer = self.question.answer_set.create(
            text="Yes, I am.",
            owner=self.user,
        )
        self.question_url = self.question.get_absolute_url()

    def test_question_detail_get(self):
        response = self.client.get(self.question_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.question.title)
        self.assertContains(response, self.answer.text)

    def test_question_detail_post_invalid_logged_out(self):
        self.client.logout()
        answer_text = ""
        response = self.client.post(self.question_url, {'text': answer_text})
        self.assertEqual(response.status_code, 302)

    def test_question_detail_post_invalid_logged_in(self):
        self.client.login(username=self.user.username,
                          password=self.user_password)
        answer_text = ""
        self.client.login(username=self.user.username,
                          password=self.user.password)
        response = self.client.post(self.question_url,
                                    {'text': answer_text},
                                    follow=True)
        self.assertContains(response, "This field is required.")

    def test_question_detail_post_valid_loged_out(self):
        answer_text = "Yet another answer"
        response = self.client.post(self.question_url, {'text': answer_text},)
        self.assertEqual(response.status_code, 302)

    def test_question_detail_post_valid_loged_in(self):
        self.client.login(username=self.user.username,
                          password=self.user_password)
        answer_text = "Yet another answer"
        response = self.client.post(self.question_url,
                                    {'text': answer_text},
                                    follow=True)
        self.assertContains(response, answer_text)

    def test_question_create_get_logged_in(self):
        self.client.login(username=self.user.username,
                          password=self.user_password)
        url = '/questions/create/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_question_create_get_not_logged_in(self):
        url = '/questions/create/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_question_create_post_not_logged_in(self):
        url = '/questions/create/'
        response = self.client.post(url, {'title': "Title"})
        self.assertEqual(response.status_code, 302)

    def test_question_delete_not_my_post_logged_in(self):
        url = '/questions/1/delete/'
        self.client.login(username=self.another_username,
                          password=self.user_password)
        sz = len(Question.objects.all())
        self.client.post(url)
        self.assertEqual(len(Question.objects.all()), sz)

    def test_question_delete_my_post_logged_in(self):
        url = '/questions/1/delete/'
        self.client.login(username=self.user.username,
                          password=self.user_password)
        sz = len(Question.objects.all())
        self.client.post(url)
        self.assertEqual(len(Question.objects.all()), sz-1)

    def test_question_update_post_not_logged_in(self):
        url = '/questions/1/delete/'
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)

    def test_question_update_not_my_post_logged_in(self):
        url = '/questions/1/update/'
        self.client.login(username=self.another_username,
                          password=self.user_password)
        self.client.post(url, {'title': "new_title",
                               'details': 'new_details'},
                         follow=True)
        self.assertEqual(Question.objects.get(pk=1).title, self.question.title)

    def test_question_update_my_post_logged_in(self):
        url = '/questions/1/update/'
        self.client.login(username=self.user.username,
                          password=self.user_password)
        response = self.client.post(url, {'title': "new_title",
                                          'details': 'new_details'},
                                    follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Question.objects.get(pk=1).title, 'new_title')

    def test_question_update_post_not_logged_in(self):
        url = '/questions/1/update/'
        response = self.client.post(url, {'title': "new_title"})
        self.assertEqual(response.status_code, 302)


class QuestionAPITest(TestCase):

    def setUp(self):
        self.username = "john_dou"
        self.user_password = "password"
        self.another_username = "john_dou_1"
        user = User.objects.create_user(username=self.username,
                                        password=self.user_password)
        User.objects.create_user(username=self.another_username,
                                 password=self.user_password)
        self.question = Question.objects.create(
            title="Title?",
            details="Details",
            owner=user,
        )

    def test_list(self):
        response = self.client.get(reverse('questions:api'))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(len(data), 1)

    def test_create_loggen_out(self):
        response = self.client.post(reverse('questions:api'),
                                    {'title': 'Title2', 'details': 'Det2'})
        self.assertEqual(response.status_code, 403)

    def test_create_loggen_in(self):
        self.client.login(username=self.username,
                          password=self.user_password)
        response = self.client.post(reverse('questions:api'),
                                    {'title': 'Title2', 'details': 'Det2'})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(len(Question.objects.all()), 2)

    def test_retrieve(self):
        url = reverse('questions:api', kwargs={'pk': self.question.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        got = json.loads(response.content.decode('utf-8'))
        data = {'title': self.question.title,
                'details': self.question.details}
        self.assertEqual(got, data)

    def test_destroy_logged_out(self):
        url = reverse('questions:api', kwargs={'pk': self.question.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 403)

    def test_destroy_not_my_logged_in(self):
        self.client.login(username=self.another_username,
                          password=self.user_password)
        url = reverse('questions:api', kwargs={'pk': self.question.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 400)

    def test_destroy_my_logged_in(self):
        self.client.login(username=self.username,
                          password=self.user_password)
        url = reverse('questions:api', kwargs={'pk': self.question.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(len(Question.objects.all()), 0)

    def test_update_logged_out(self):
        url = reverse('questions:api', kwargs={'pk': self.question.pk})
        data = json.dumps({'title': 'new_title', 'details': 'new_details'})
        response = self.client.put(url, data, content_type='application/json')
        self.assertEqual(response.status_code, 403)

    def test_update_not_my_logged_in(self):
        self.client.login(username=self.another_username,
                          password=self.user_password)
        url = reverse('questions:api', kwargs={'pk': self.question.pk})
        data = json.dumps({'title': 'new_title', 'details': 'new_details'})
        response = self.client.put(url, data, content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_update_my_logged_in(self):
        self.client.login(username=self.username,
                          password=self.user_password)
        url = reverse('questions:api', kwargs={'pk': self.question.pk})
        data = json.dumps({'title': 'new_title', 'details': 'new_details'})
        response = self.client.put(url, data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Question.objects.all()[0].title, 'new_title')
