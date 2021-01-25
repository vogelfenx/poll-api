from django.contrib import admin
from .models import Poll, Choice, Vote
from django.urls import resolve


class VoteInline(admin.TabularInline):
    model = Vote

    # def get_parent_object_from_request(self, request):
    #     """
    #     Returns the parent object from the request or None.

    #     Note that this only works for Inlines, because the `parent_model`
    #     is not available in the regular admin.ModelAdmin as an attribute.
    #     """
    #     # breakpoint()
    #     resolved = resolve(request.path_info)
    #     if resolved.kwargs:
    #         return resolved.kwargs['object_id']
    #     return None

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        parent_id = request.resolver_match.kwargs.get('object_id')
        kwargs['queryset'] = Choice.objects.filter(poll=parent_id)

        return super(VoteInline, self).formfield_for_foreignkey(db_field, request, **kwargs)


class PollAdmin(admin.ModelAdmin):
    readonly_fields = ('created_by', 'pub_date',)
    list_display = ('question', 'created_by', 'pub_date')

    inlines = [
        VoteInline,
    ]


class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('poll', 'choice_text',)


admin.site.register(Poll, PollAdmin)
admin.site.register(Choice, ChoiceAdmin)
# admin.site.register(Vote, VoteAdmin)
