from django.contrib import admin
from .models import Event, Profile, Detachment, Institution, EventKind, EventColor, Mark, Area


class EvAdmin(admin.ModelAdmin):
    list_display = ('name', 'content', 'beginning_date')
    list_display_links = ('name', 'content')
    search_fields = ('name', 'content')


class EvKind(admin.ModelAdmin):
    list_display = ('name',)
    list_display_links = ('name',)
    search_fields = ('name',)


admin.site.register(Event, EvAdmin)
admin.site.register(Profile)
admin.site.register(Detachment)
admin.site.register(Institution)
admin.site.register(EventKind, EvKind)
admin.site.register(EventColor)
admin.site.register(Mark)
admin.site.register(Area)
