from django.test import TestCase
from django.contrib.auth.models import User
from .models import Post, Comment


class PostTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass123")

    def test_post_creation(self):
        post = Post.objects.create(author=self.user, content="Hello world", visibility="public")
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(post.author, self.user)
        self.assertEqual(post.total_likes(), 0)

    def test_post_like(self):
        post = Post.objects.create(author=self.user, content="Test", visibility="public")
        post.likes.add(self.user)
        self.assertEqual(post.total_likes(), 1)


class CommentTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass123")
        self.post = Post.objects.create(author=self.user, content="Post", visibility="public")

    def test_comment_creation(self):
        Comment.objects.create(post=self.post, author=self.user, text="A comment")
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(self.post.comments.count(), 1)
