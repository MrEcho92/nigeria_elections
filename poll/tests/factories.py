import random
import string

from poll.models import Choice, Question

_RANDOM_ALUM = string.ascii_lowercase + string.digits


def random_string(alphabet=_RANDOM_ALUM, length=10):
    return "".join(random.choice(alphabet) for i in range(length))


def question_factory(**kwargs):
    fuzz = random_string()
    status = kwargs.pop("status", Question.DRAFT)
    question_text = kwargs.pop("question_text", fuzz)

    create_kwargs = dict(
        {"status": status, "question_text": question_text},
        **kwargs,
    )

    return Question.objects.create(**create_kwargs)


def choice_factory(**kwargs):
    fuzz = random_string()
    choice_text = kwargs.pop("choice_text", fuzz)
    question = kwargs.pop("question", None) or question_factory()

    create_kwargs = dict(
        {"choice_text": choice_text, "question": question},
        **kwargs,
    )

    return Choice.objects.create(**create_kwargs)
