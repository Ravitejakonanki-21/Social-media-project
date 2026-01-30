from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q
from .models import FriendRequest, Follow


@login_required
def friend_list_view(request):
    # Accepted friend requests
    accepted = FriendRequest.objects.filter(
        Q(sender=request.user) | Q(receiver=request.user)
    ).filter(accepted=True)
    friends = []
    for fr in accepted:
        other = fr.receiver if fr.sender == request.user else fr.sender
        friends.append(other)
    # Pending sent/received
    sent = FriendRequest.objects.filter(sender=request.user, accepted=False)
    received = FriendRequest.objects.filter(receiver=request.user, accepted=False)
    return render(request, "friends/list.html", {
        "friends": friends,
        "sent_requests": sent,
        "received_requests": received,
    })


@login_required
def send_friend_request_view(request, username):
    other = get_object_or_404(User, username=username)
    if other == request.user:
        messages.error(request, "You cannot send a request to yourself.")
        return redirect("users:profile", username=username)
    if FriendRequest.objects.filter(sender=request.user, receiver=other).exists():
        messages.info(request, "Request already sent.")
        return redirect("users:profile", username=username)
    if FriendRequest.objects.filter(sender=other, receiver=request.user).exists():
        messages.info(request, "They already sent you a request. Accept it from Friends.")
        return redirect("users:profile", username=username)
    FriendRequest.objects.create(sender=request.user, receiver=other)
    messages.success(request, f"Friend request sent to {other.username}.")
    return redirect("users:profile", username=username)


@login_required
def accept_friend_request_view(request, pk):
    fr = get_object_or_404(FriendRequest, pk=pk, receiver=request.user)
    fr.accepted = True
    fr.save()
    messages.success(request, f"You are now friends with {fr.sender.username}.")
    return redirect(request.META.get("HTTP_REFERER", "friends:list"))


@login_required
def follow_view(request, username):
    other = get_object_or_404(User, username=username)
    if other == request.user:
        messages.error(request, "You cannot follow yourself.")
        return redirect("users:profile", username=username)
    Follow.objects.get_or_create(follower=request.user, following=other)
    messages.success(request, f"You are now following {other.username}.")
    return redirect("users:profile", username=username)


@login_required
def unfollow_view(request, username):
    other = get_object_or_404(User, username=username)
    Follow.objects.filter(follower=request.user, following=other).delete()
    messages.info(request, f"You unfollowed {other.username}.")
    return redirect("users:profile", username=username)
