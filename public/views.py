import logging

from django.contrib.gis.geoip2 import GeoIP2
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from geoip2.errors import AddressNotFoundError

from poll.constants import Countries, States
from poll.forms import VoteForm
from poll.models import Choice, Question, Vote

logger = logging.getLogger(__name__)


def aboutus(request):
    return render(request, "about.html")


def index(request):
    return render(request, "index.html")


def candidates_info(request):
    question = Question.active()

    context = {
        "question": question,
        "error": {},
    }

    if question is not None:
        question_choices = question.choices.all()

        result = question.compute_result()

        context.update(
            {
                "choices": question_choices,
                "total": result["total_vote"],
                "choice_percent": result["choice_by_percent"],
            }
        )

    if request.method == "POST":
        try:
            selected_choice = question_choices.get(pk=request.POST["choice"])
        except (KeyError, Choice.DoesNotExist):
            context["error"]["error_message"] = "You didn't select a choice."
        else:
            selected_choice.votes += 1
            selected_choice.save()

            return redirect("public:candidates-info")

    return render(request, "candidates_info.html", context=context)


def create_vote(request):
    ip_address = _get_ip_address(request)
    try:
        # Both country & city database stored in dir (geolocation/)
        g = GeoIP2()
        country = g.country_name(ip_address)
    except AddressNotFoundError as e:
        logger.info("IP Address invalid: %s", e)
        country = "Nigeria"

    if request.method == "POST":
        form = VoteForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.ip_address = ip_address
            if not request.session.session_key:
                request.session.save()
            instance.user_identifier = request.session.session_key
            instance.save()
            return redirect("public:cast-vote", vote_id=instance.id)
    else:
        form = VoteForm()

    ctx = {
        "country": country.upper(),
        "form": form,
        "states": dict(States),
        "countries": dict(Countries),
        "already_voted": Vote.objects.filter(
            ip_address=ip_address, voted=True
        ).exists(),
    }

    return render(request, "vote_create.html", ctx)


def vote_detail(request, vote_id):
    vote = get_object_or_404(Vote, pk=vote_id)

    if vote.user_identifier != request.session.session_key:
        return HttpResponseForbidden()

    if request.method == "POST":
        candidate = request.POST["candidate"]
        if candidate not in dict(Vote.CANDIDATES).keys():
            return HttpResponseForbidden()

        vote.candidate = candidate
        vote.save()
        return redirect("public:vote-success")

    return render(request, "vote.html", {"vote": vote})


def vote_success(request):
    candidates = dict(Vote.CANDIDATES)
    result = _get_vote_result(candidates)
    return render(request, "vote_success.html", {"result": result})


def _get_ip_address(request):
    if x_forwarded_for := request.META.get("HTTP_X_FORWARDED_FOR"):
        ip_address = x_forwarded_for.split(",")[0]
    else:
        ip_address = request.META.get("REMOTE_ADDR")

    return ip_address


def _get_vote_result(candidates):
    total_count = Vote.objects.filter(voted=True).count()
    result = {
        v: round(Vote.get_candidate_count(k) / total_count * 100)
        if total_count
        else None
        for k, v in candidates.items()
    }
    logger.info("Voting result: %s", result)
    return result
