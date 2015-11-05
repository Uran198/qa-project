from django.test import TestCase

from .models import Question


class QuestionTest(TestCase):

    def test_save(self):
        question = Question(
            title="Are you o'kay?",
        )
        question.save()
        self.assertEqual(question.slug, "are-you-okay")


class AnswerTest(TestCase):

    def test_get_absolute_url(self):
        question = Question.objects.create(
            title="Title?"
        )
        answer = question.answer_set.create(
            text="Answer"
        )
        self.assertEqual(answer.get_absolute_url(),
                         question.get_absolute_url())
