import random
import string

from poll.models import Choice, Question, Vote

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
    votes = kwargs.pop("votes", 0)

    create_kwargs = dict(
        {"choice_text": choice_text, "question": question, "votes": votes},
        **kwargs,
    )

    return Choice.objects.create(**create_kwargs)


def vote_factory(**kwargs):

    ip_address = kwargs.pop("ip_address", random_string())
    user_identifier = kwargs.pop("user_identifier", random_string())
    country = kwargs.pop("country", "")
    state = kwargs.pop("state", "")
    voted = kwargs.pop("voted", False)
    candidate = kwargs.pop("candidate", "")

    create_kwargs = dict(
        {
            "ip_address": ip_address,
            "user_identifier": user_identifier,
            "country": country,
            "state": state,
            "voted": voted,
            "candidate": candidate,
        },
        **kwargs,
    )

    return Vote.objects.create(**create_kwargs)
