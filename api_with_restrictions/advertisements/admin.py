from django.contrib import admin
from .models import Advertisement


@admin.register(Advertisement)
class ScopeAdmin(admin.ModelAdmin):
    pass