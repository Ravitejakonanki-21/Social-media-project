def recent_notifications(request):
    if request.user.is_authenticated:
        from .models import Notification
        return {
            "recent_notifications": Notification.objects.filter(user=request.user).order_by("-created_at")[:10],
            "unread_count": Notification.objects.filter(user=request.user, is_read=False).count(),
        }
    return {"recent_notifications": [], "unread_count": 0}
