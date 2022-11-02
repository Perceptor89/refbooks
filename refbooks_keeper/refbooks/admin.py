from django.contrib import admin
from .models import Refbook, Version, Element
from .forms import RefbookForm, VersionForm, ElementAdminForm


admin.site.site_title = 'Refbooks admin panel'
admin.site.site_header = 'Refbooks admin panel'


@admin.register(Refbook)
class RefbookAdmin(admin.ModelAdmin):
    form = RefbookForm
    list_display = ('id', 'code', 'name', 'description')
    ordering = ['id']


class ElementInline(admin.TabularInline):
    model = Element
    extra = 1


@admin.register(Version)
class VersionAdmin(admin.ModelAdmin):
    form = VersionForm
    list_display = ('id', 'name', 'start_date', 'refbook_code', 'refbook')
    readonly_fields = ('refbook_code',)
    list_filter = ('start_date', ('refbook', admin.RelatedOnlyFieldListFilter))
    inlines = [ElementInline]
    ordering = ['id']

    @admin.display(description='Refbook code')
    def refbook_code(self, instance):
        return instance.refbook.code


@admin.register(Element)
class ElementAdmin(admin.ModelAdmin):
    form = ElementAdminForm
    list_display = ('id', 'code', 'value', 'refbook_code', 'version')
    readonly_fields = ('refbook_code',)
    list_filter = (
        'version',
        ('version__refbook', admin.RelatedOnlyFieldListFilter),
    )
    ordering = ['id']

    @admin.display(description='Refbook code')
    def refbook_code(self, instance):
        return instance.version.refbook.code
