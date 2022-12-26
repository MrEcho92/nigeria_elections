from django.db import models
from gcloudc.db import transaction
from gcloudc.db.models.fields.charfields import CharField

from core.models import TimeStampModel

from .constants import Countries, States


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

        return result

    def __str__(self) -> str:
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


class Vote(TimeStampModel):
    """
    Voting entity to capture selected candidate for a user
    """

    ATIKU_ABUBAKAR = "ATIKU_ABUBAKAR"
    PETER_OBI = "PETER_OBI"
    BOLA_AHMED_TINUBU = "BOLA_AHMED_TINUBU"
    OMOYELE_SOWORE = "OMOYELE_SOWORE"

    CANDIDATES = (
        (ATIKU_ABUBAKAR, "Atiku Abubakar"),
        (PETER_OBI, "Peter Obi"),
        (BOLA_AHMED_TINUBU, "Bola Ahmed Tinubu"),
        (OMOYELE_SOWORE, "Omoyele Sowore"),
    )

    ip_address = models.CharField(max_length=100)
    user_identifier = models.CharField(
        max_length=100, help_text="Stores user session cookie", unique=True
    )
    country = models.CharField(max_length=100, choices=Countries, blank=True)
    state = models.CharField(max_length=100, choices=States, blank=True)
    voted = models.BooleanField(default=False)
    candidate = models.CharField(max_length=100, choices=CANDIDATES, blank=True)

    def __str__(self) -> str:
        return f"Voted for {self.candidate} by {self.user_identifier}"

    @classmethod
    def get_candidate_count(cls, candidate) -> int:
        return cls.objects.filter(candidate=candidate).count()

    class Meta:
        unique_together = ("user_identifier", "ip_address")
