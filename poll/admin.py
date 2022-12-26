from django.contrib import admin

from core.admin import admin_site
from poll.models import Choice, Question, Vote


class ChoiceInline(admin.TabularInline):
    model = Choice
    fields = ("choice_text", "votes")
    extra = 1


@admin.register(Question, site=admin_site)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("question_text", "status")
    readonly_fields = (
        "created_at",
        "modified_at",
        "created_by",
        "modified_by",
    )
    inlines = [ChoiceInline]

    def save_model(self, request, obj, form, change):
        if not obj.created_by:
            obj.created_by = request.user

        obj.modified_by = request.user
        return super().save_model(request, obj, form, change)


@admin.register(Vote, site=admin_site)
class VoteAdmin(admin.ModelAdmin):
    pass
