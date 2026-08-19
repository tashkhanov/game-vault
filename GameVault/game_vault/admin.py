from django.contrib import admin
from .models import *

admin.site.register(Genre)
# admin.site.register(Game)
admin.site.register(Mod)
admin.site.register(SystemRequirements)
admin.site.register(News)
admin.site.register(Comment)


class RequirementsInline(admin.TabularInline):
    model = SystemRequirements
    fk_name = 'game'
    extra = 1


class GameImageInline(admin.TabularInline):
    model = GameImage
    extra = 1


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'developer', 'released', 'created_at')
    inlines = [RequirementsInline, GameImageInline]
    list_display_links = ('id', 'title',)
