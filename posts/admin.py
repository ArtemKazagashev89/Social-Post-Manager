from django.contrib import admin

from .models import Comment, Post, User


class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "created_at", "updated_at")  # Поля, отображаемые в списке
    list_filter = ("created_at",)  # Фильтр по дате создания
    search_fields = ("title", "text")  # Поля для поиска
    ordering = ("-created_at",)  # Сортировка по убыванию даты создания


class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "phone_number", "birth_date", "created_at")  # Поля, отображаемые в списке


class CommentAdmin(admin.ModelAdmin):
    list_display = ("author", "post", "created_at", "updated_at")  # Поля, отображаемые в списке


# Регистрация моделей в админ-панели
admin.site.register(User, UserAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
