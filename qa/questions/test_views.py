import json

from django.test import TestCase, RequestFactory
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

# from .views import QuestionDetailView
from .models import Question


class QuestionViewsTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user_password = "password"
        self.user = User.objects.create_user(
            username="John", email="john@dou.com", password=self.user_password)
        self.question = Question.objects.create(
            title="Are you allright?"
        )
        self.answer = self.question.answer_set.create(
            text="Yes, I am."
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

    def test_question_detail_post_valid_looged_out(self):
        answer_text = "Yet another answer"
        response = self.client.post(self.question_url, {'text': answer_text},)
        self.assertEqual(response.status_code, 302)

    def test_question_detail_post_valid_looged_in(self):
        self.client.login(username=self.user.username,
                          password=self.user_password)
        answer_text = "Yet another answer"
        response = self.client.post(self.question_url,
                                    {'text': answer_text},
                                    follow=True)
        self.assertContains(response, answer_text)


class QuestionAPITest(TestCase):

    def setUp(self):
        self.username = "john_dou"
        self.user_password = "password"
        User.objects.create_user(username=self.username,
                                 password=self.user_password)
        self.question = Question.objects.create(
            title="Title?",
            details="Details",
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

    def test_destroy_logged_in(self):
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

    def test_update_logged_in(self):
        self.client.login(username=self.username,
                          password=self.user_password)
        url = reverse('questions:api', kwargs={'pk': self.question.pk})
        data = json.dumps({'title': 'new_title', 'details': 'new_details'})
        response = self.client.put(url, data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Question.objects.all()[0].title, 'new_title')
