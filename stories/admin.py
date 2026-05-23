from django.contrib import admin
from .models import Story

@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at', 'view_count')

    def view_count(self, obj):
        return obj.views.count()