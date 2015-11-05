from django.test import TestCase, Client
# from django.core.urlresolvers import reverse

# from .views import QuestionDetailView
from .models import Question


class QuestionViewsTest(TestCase):

    def setUp(self):
        self.client = Client()
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
