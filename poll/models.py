from django.db import models
from gcloudc.db import transaction
from gcloudc.db.models.fields.charfields import CharField

from core.models import TimeStampModel


class Question(TimeStampModel):
    """Class for individual question"""

    DRAFT = "DRAFT"
    ACTIVE = "ACTIVE"
    CLOSED = "CLOSED"

    STATUSES = ((DRAFT, "Draft"), (ACTIVE, "Active"), (CLOSED, "Closed"))

    question_text = models.TextField()
    status = CharField(choices=STATUSES, default=DRAFT)

    @classmethod
    def active(cls):
        try:
            return cls.objects.get(status=cls.ACTIVE)
        except cls.DoesNotExist:
            return None

    def compute_result(self):
        result = {"total_vote": 0, "choice_by_percent": {}}
        choices = self.choices.all()

        total_votes = 0
        choice_total = []
        for choice in choices:
            total_votes += choice.votes
            choice_total.append((choice.id, choice.votes))

        if total_votes:
            for choice_id, vote in choice_total:
                result["choice_by_percent"][choice_id] = round(vote / total_votes * 100)
            result["total_vote"] = total_votes
        else:
            result["total_vote"] = 0

        return result

    def __str__(self):
        return f"{self.question_text} - {self.status}"

    def save(self, *args, **kwargs):
        klass = type(self)

        if self.status == klass.ACTIVE:
            # enforce only one question to be active
            with transaction.atomic():
                klass.objects.filter(status=klass.ACTIVE).exclude(id=self.id).update(
                    status=klass.CLOSED
                )
                return super().save(*args, **kwargs)

        return super().save(*args, **kwargs)


class Choice(TimeStampModel):
    choice_text = CharField()
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="choices"
    )
    votes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.choice_text} - {self.votes}"
