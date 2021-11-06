from django.contrib import admin
from .models import *

@admin.register(Programm)
class ProgrammAdmin(admin.ModelAdmin):
    list_display = ("name", "min_credit", "max_credit", "min_age", "max_age")


@admin.register(Borrower)
class BorrowerAdmin(admin.ModelAdmin):
    list_display = ("id", "uin", "birthday")


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ("amount", "status", "rejection_reason" )


@admin.register(BlackList)
class BlackListAdmin(admin.ModelAdmin):
    list_display = ("uin",)