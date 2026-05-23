from django.urls import path
from .views import*

urlpatterns = [
    path('', story_list, name='stories'),
    path('add/', add_story, name='add_story'),
    path('view/', story_view, name='story_view'),
    path('view/<int:story_id>/', mark_story_view, name='mark_story_view'),
     path('viewers/<int:story_id>/', story_viewers, name='story_viewers'),
]