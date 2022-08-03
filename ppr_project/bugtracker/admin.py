from django.contrib import admin

from bugtracker.models import Bug


@admin.register(Bug)
class BugAdmin(admin.ModelAdmin):
    list_display = (
        'type', 'pub_date', 'close_date', 'bug_description', 'author'
    )
