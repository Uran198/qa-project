from django.test import TestCase
from django.contrib.auth.models import User

from .models import Question


class QuestionTest(TestCase):

    def test_save(self):
        user = User.objects.create_user(
            username="username",
            password="password",
        )
        question = Question(
            title="Are you o'kay?",
            owner=user,
        )
        question.save()
        self.assertEqual(question.slug, "are-you-okay")


class AnswerTest(TestCase):

    def test_get_absolute_url(self):
        user = User.objects.create_user(
            username="username",
            password="password",
        )
        question = Question.objects.create(
            title="Title?",
            owner=user,
        )
        answer = question.answer_set.create(
            text="Answer",
            owner=user,
        )
        self.assertEqual(answer.get_absolute_url(),
                         question.get_absolute_url())
