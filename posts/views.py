from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Q
from .models import Post, Comment
from .forms import PostForm, CommentForm


def feed_view(request):
    """Feed: public posts + friends-only posts if user is friend of author."""
    if not request.user.is_authenticated:
        return render(request, "posts/feed.html", {"posts": [], "query": ""})
    from friends.models import FriendRequest, Follow
    # Users the current user is "friends" with (accepted requests)
    friend_ids = set()
    for fr in FriendRequest.objects.filter(Q(sender=request.user) | Q(receiver=request.user)).filter(accepted=True):
        friend_ids.add(fr.sender_id)
        friend_ids.add(fr.receiver_id)
    friend_ids.discard(request.user.id)
    # Users we follow (optional: treat as friends for visibility)
    following_ids = set(Follow.objects.filter(follower=request.user).values_list("following_id", flat=True))
    can_see = friend_ids | following_ids | {request.user.id}
    posts = Post.objects.filter(
        Q(visibility="public") | (Q(visibility="friends") & Q(author_id__in=can_see))
    ).select_related("author").prefetch_related("likes", "comments").order_by("-created_at")[:50]
    query = request.GET.get("q", "").strip()
    if query:
        posts = posts.filter(content__icontains=query)
    return render(request, "posts/feed.html", {"posts": posts, "query": query})


@login_required
def create_post_view(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, "Post created.")
            return redirect("/")
        messages.error(request, "Please fix the errors.")
    else:
        form = PostForm()
    return render(request, "posts/create_post.html", {"form": form})


@login_required
@require_POST
def like_post_view(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
    return JsonResponse({"liked": liked, "total_likes": post.total_likes()})


@login_required
@require_POST
def comment_post_view(request, pk):
    post = get_object_or_404(Post, pk=pk)
    form = CommentForm(request.POST)
    if form.is_valid():
        Comment.objects.create(post=post, author=request.user, text=form.cleaned_data["text"])
        messages.success(request, "Comment added.")
    else:
        messages.error(request, "Invalid comment.")
    return redirect(request.META.get("HTTP_REFERER", "/"))


@login_required
def delete_post_view(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user:
        messages.error(request, "Not allowed.")
        return redirect("/")
    post.delete()
    messages.success(request, "Post deleted.")
    return redirect(request.META.get("HTTP_REFERER", "/"))
