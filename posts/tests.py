from datetime import date

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Comment, Post, User


class UserTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="Test1234!",
            email="testuser@mail.ru",  # Изменено на разрешенный домен
            phone_number="1234567890",
            birth_date=date(2000, 1, 1),
        )

    def test_user_creation(self):
        self.assertEqual(User.objects.count(), 1)


class PostTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="Test1234!",
            email="testuser@mail.ru",  # Изменено на разрешенный домен
            phone_number="1234567890",
            birth_date=date(2000, 1, 1),
        )
        self.client.login(username="testuser", password="Test1234!")
        self.post = Post.objects.create(title="Test Post", text="This is a test post.", author=self.user)

    def test_create_post(self):
        response = self.client.post(
            reverse("post-list"),
            {"title": "New Test Post", "text": "This is another test post.", "author": self.user.id},
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 2)

    def test_get_posts(self):
        response = self.client.get(reverse("post-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_update_post(self):
        response = self.client.put(
            reverse("post-detail", args=[self.post.id]),
            {"title": "Updated Test Post", "text": "This post has been updated.", "author": self.user.id},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, "Updated Test Post")

    def test_delete_post(self):
        response = self.client.delete(reverse("post-detail", args=[self.post.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Post.objects.count(), 0)


class CommentTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="Test1234!",
            email="testuser@mail.ru",
            phone_number="1234567890",
            birth_date=date(2000, 1, 1),
        )
        self.post = Post.objects.create(title="Test Post", text="This is a test post.", author=self.user)
        self.client.login(username="testuser", password="Test1234!")

    def test_create_comment(self):
        response = self.client.post(
            reverse("comment-list"), {"post": self.post.id, "text": "This is a comment.", "author": self.user.id}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 1)

    def test_update_comment(self):
        comment = Comment.objects.create(post=self.post, author=self.user, text="Original comment.")
        response = self.client.put(
            reverse("comment-detail", args=[comment.id]),
            {"post": self.post.id, "text": "Updated comment.", "author": self.user.id},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        comment.refresh_from_db()
        self.assertEqual(comment.text, "Updated comment.")

    def test_delete_comment(self):
        comment = Comment.objects.create(post=self.post, author=self.user, text="Comment to delete.")
        response = self.client.delete(reverse("comment-detail", args=[comment.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Comment.objects.count(), 0)
