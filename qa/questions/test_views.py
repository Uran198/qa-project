import json

from django.test import TestCase
from django.core.urlresolvers import reverse

# from .views import QuestionDetailView
from .models import Question


class QuestionViewsTest(TestCase):

    def setUp(self):
        self.question = Question.objects.create(
            title="Are you allright?"
        )
        self.answer = self.question.answer_set.create(
            text="Yes, I am."
        )

    def test_question_detail_get(self):
        response = self.client.get(self.question.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.question.title)
        self.assertContains(response, self.answer.text)

    def test_question_detail_post_invalid(self):
        answer_text = ""
        response = self.client.post(self.question.get_absolute_url(),
                                    {'text': answer_text},
                                    follow=True)
        self.assertContains(response, "This field is required.")

    def test_question_detail_post_valid(self):
        answer_text = "Yet another answer"
        response = self.client.post(self.question.get_absolute_url(),
                                    {'text': answer_text},
                                    follow=True)
        self.assertContains(response, answer_text)


class QuestionAPITest(TestCase):

    def setUp(self):
        self.question = Question.objects.create(
            title="Title?",
            details="Details",
        )

    def test_list(self):
        response = self.client.get(reverse('questions:api'))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(len(data), 1)

    def test_create(self):
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

    def test_destroy(self):
        url = reverse('questions:api', kwargs={'pk': self.question.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(len(Question.objects.all()), 0)

    def test_update(self):
        url = reverse('questions:api', kwargs={'pk': self.question.pk})
        data = json.dumps({'title': 'new_title', 'details': 'new_details'})
        response = self.client.put(url, data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Question.objects.all()[0].title, 'new_title')
