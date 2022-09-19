from django.shortcuts import redirect, render

from poll.models import Choice, Question


def index(request):

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

            return redirect("public:index")

    return render(request, "index.html", context=context)
