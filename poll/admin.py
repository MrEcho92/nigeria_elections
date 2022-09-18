from django.contrib import admin

from core.admin import admin_site
from poll.models import Choice, Question


@admin.register(Question, site=admin_site)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("question_text", "status")
    readonly_fields = (
        "created_at",
        "modified_at",
        "created_by",
        "modified_by",
    )

    def save_model(self, request, obj, form, change):
        if not obj.created_by:
            obj.created_by = request.user

        obj.modified_by = request.user
        return super().save_model(request, obj, form, change)


@admin.register(Choice, site=admin_site)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ("choice_text", "votes")
    readonly_fields = (
        "created_at",
        "modified_at",
        "created_by",
        "modified_by",
        "question",
    )

    def save_model(self, request, obj, form, change):
        if not obj.created_by:
            obj.created_by = request.user

        # We may change this in future to allow for admin to select question
        if not obj.question_id:
            obj.question = Question.objects.get(status=Question.ACTIVE)

        obj.modified_by = request.user
        return super().save_model(request, obj, form, change)
