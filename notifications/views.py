from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import Notification


@login_required
def notification_list_view(request):
    notifications = Notification.objects.filter(user=request.user).order_by("-created_at")[:50]
    return render(request, "notifications/list.html", {"notifications": notifications})


@login_required
@require_POST
def mark_read_view(request, pk):
    n = Notification.objects.filter(user=request.user, pk=pk).first()
    if n:
        n.is_read = True
        n.save()
    return redirect(request.META.get("HTTP_REFERER", "/"))
