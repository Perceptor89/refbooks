from django.contrib import admin
from .models import Refbook, Version, Element
from .forms import RefbookForm, VersionForm, ElementAdminForm


@admin.register(Refbook)
class RefbookAdmin(admin.ModelAdmin):
    form = RefbookForm
    list_display = ('id', 'code', 'name', 'description')


class ElementInline(admin.TabularInline):
    model = Element
    extra = 1


@admin.register(Version)
class VersionAdmin(admin.ModelAdmin):
    form = VersionForm
    list_display = ('id', 'name', 'start_date', 'refbook')
    inlines = [ElementInline]


@admin.register(Element)
class ElementAdmin(admin.ModelAdmin):
    form = ElementAdminForm
    list_display = ('id', 'code', 'name', 'version')
