from djangae.test import TestCase

from poll.models import Choice, Question

from .factories import choice_factory, question_factory


class QuestionModel(TestCase):
    def test_create_question(self):
        self.assertEqual(Question.objects.count(), 0)

        question_factory()
        question_factory()

        self.assertEqual(Question.objects.count(), 2)

    def test_only_one_active_question_allowed(self):
        q1 = question_factory(status=Question.ACTIVE)

        self.assertEqual(q1.status, Question.ACTIVE)

        q2 = question_factory(status=Question.ACTIVE)

        q1.refresh_from_db()

        self.assertEqual(q1.status, Question.CLOSED)
        self.assertEqual(q2.status, Question.ACTIVE)

    def test_active_question(self):
        q1 = question_factory(status=Question.ACTIVE)

        self.assertEqual(Question.active(), q1)

    def test_compute_result(self):
        question = question_factory()
        c1 = choice_factory(question=question)
        c2 = choice_factory(question=question)

        c1.votes = 1
        c1.save()

        c2.votes = 1
        c2.save()
        # Total vote ~= 2 (c1.vote + c2.vote)
        result = question.compute_result()
        self.assertEqual(result["total_vote"], 2)

        # 50% for the choices
        self.assertEqual(result["choice_by_percent"][c1.id], 50)
        self.assertEqual(result["choice_by_percent"][c2.id], 50)


class ChoiceModel(TestCase):
    def test_create_choice(self):
        self.assertEqual(Choice.objects.count(), 0)

        choice_factory()
        choice_factory()

        self.assertEqual(Choice.objects.count(), 2)
