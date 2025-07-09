import re
from datetime import timedelta

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    phone_number = models.CharField(max_length=15)
    birth_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "users"

    def clean(self):
        super().clean()
        # Валидатор для пароля
        if len(self.password) < 8 or not re.search(r"\d", self.password):
            raise ValidationError("Пароль должен содержать не менее 8 символов и включать цифры.")

    def save(self, *args, **kwargs):
        self.full_clean()
        if not self.email.endswith(("@mail.ru", "@yandex.ru")):
            raise ValidationError("Почта должна быть с доменом mail.ru или yandex.ru.")
        super().save(*args, **kwargs)


class Post(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()
    image = models.ImageField(upload_to="posts/", blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "posts"
        ordering = ["-created_at"]

    def clean(self):
        super().clean()
        # Проверка возраста автора
        if self.author.birth_date > (timezone.now() - timedelta(days=6570)).date():  # 18 лет
            raise ValidationError("Автор должен быть старше 18 лет.")

        # Проверка заголовка на запрещенные слова
        forbidden_words = ["ерунда", "глупость", "чепуха"]
        if any(word in self.title.lower() for word in forbidden_words):
            raise ValidationError("Заголовок не должен содержать запрещенные слова.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "comments"
        ordering = ["-created_at"]
