from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta

from .models import Story, StoryView


@login_required
def mark_story_view(request, story_id):
    story = get_object_or_404(Story, id=story_id)

    StoryView.objects.get_or_create(
        story=story,
        user=request.user
    )

    return JsonResponse({'status': 'ok'})


def story_view(request):
    last_24 = timezone.now() - timedelta(hours=24)

    stories = Story.objects.filter(
        created_at__gte=last_24,
        is_active=True
    )

    return render(request, 'stories/story_view.html', {
        'stories': stories
    })


def story_viewers(request, story_id):
    story = get_object_or_404(Story, id=story_id)

    viewers = story.views.select_related('user')

    data = []
    for v in viewers:
        data.append({
            'phone': v.user.phone if v.user else ''
        })

    return JsonResponse({'viewers': data})


@login_required
def add_story(request):
    if not request.user.is_staff:
        return redirect('dashboard')

    if request.method == 'POST':
        Story.objects.create(
            user=request.user,
            image=request.FILES.get('image'),
            video=request.FILES.get('video')
        )
        return redirect('dashboard')

    return render(request, 'stories/add_story.html')


def story_list(request):
    last_24_hours = timezone.now() - timedelta(hours=24)

    stories = Story.objects.filter( created_at__gte=last_24_hours, is_active=True ).order_by('-created_at')

    return render(request, 'stories/story_list.html', { 'stories': stories })