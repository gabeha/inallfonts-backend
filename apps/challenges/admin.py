from .models import Challenge, Response, Interaction

from django.contrib import admin

admin.site.register(
    [Interaction]
)


@admin.register(Challenge)
class ChallengeAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'user', 'tags_list', 'created_at')

    def tags_list(self, obj):
        return ", ".join(tag.name for tag in obj.tags.all())
    tags_list.short_description = 'Tags'


@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):
    list_display = ('challenge', 'user', 'title',
                    'description', 'image', 'tags_list')

    def tags_list(self, obj):
        return ", ".join(tag.name for tag in obj.tags.all())
    tags_list.short_description = 'Tags'
