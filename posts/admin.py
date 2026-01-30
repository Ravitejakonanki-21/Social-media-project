from django.contrib import admin
from .models import Post, Comment


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["author", "content_preview", "visibility", "created_at"]
    list_filter = ["visibility", "created_at"]
    search_fields = ["content", "author__username"]
    inlines = [CommentInline]

    def content_preview(self, obj):
        return obj.content[:50] + "..." if len(obj.content) > 50 else obj.content
    content_preview.short_description = "Content"


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["post", "author", "text_preview", "created_at"]
    search_fields = ["text", "author__username"]

    def text_preview(self, obj):
        return obj.text[:40] + "..." if len(obj.text) > 40 else obj.text
    text_preview.short_description = "Text"
