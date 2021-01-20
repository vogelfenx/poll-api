from django.contrib import admin
from .models import Poll


class PollAdmin(admin.ModelAdmin):
    readonly_fields = ('created_by', 'pub_date',)
    list_display = ('question', 'created_by', 'pub_date')


admin.site.register(Poll, PollAdmin)
