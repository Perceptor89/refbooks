from django.contrib import admin
from .models import Refbook, Version, Element
from .forms import RefbookForm


@admin.register(Refbook)
class RefbookAdmin(admin.ModelAdmin):
    form = RefbookForm
    list_display = (
        'id',
        'code',
        'name',
        'description'
    )

# admin.site.register(Refbook)
# admin.site.register(Version)
# admin.site.register(Element)
