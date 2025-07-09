from rest_framework import permissions, viewsets

from .models import Comment, Post, User
from .serializers import CommentSerializer, PostSerializer, UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return User.objects.filter(id=user.id)  # Возвращаем только текущего авторизованного пользователя
        return User.objects.none()  # Если пользователь не авторизован, возвращаем пустой QuerySet


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)  # Устанавливаем автора поста как текущего пользователя

    def get_queryset(self):
        return Post.objects.all()  # Возвращаем все посты

    def perform_update(self, serializer):
        post = self.get_object()
        if post.author == self.request.user or self.request.user.is_staff:
            serializer.save()  # Сохраняем изменения, если пользователь автор поста или администратор
        else:
            raise permissions.PermissionDenied("У вас нет прав для редактирования этого поста.")  # Ошибка доступа

    def perform_destroy(self, instance):
        if instance.author == self.request.user or self.request.user.is_staff:
            instance.delete()  # Удаляем пост, если пользователь автор поста или администратор
        else:
            raise permissions.PermissionDenied("У вас нет прав для удаления этого поста.")  # Ошибка доступа


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)  # Устанавливаем автора комментария как текущего пользователя

    def get_queryset(self):
        return Comment.objects.all()  # Возвращаем все комментарии

    def perform_update(self, serializer):
        comment = self.get_object()
        if comment.author == self.request.user or self.request.user.is_staff:
            serializer.save()  # Сохраняем изменения, если пользователь автор комментария или администратор
        else:
            raise permissions.PermissionDenied(
                "У вас нет прав для редактирования этого комментария."
            )  # Ошибка доступа

    def perform_destroy(self, instance):
        if instance.author == self.request.user or self.request.user.is_staff:
            instance.delete()  # Удаляем комментарий, если пользователь автор комментария или администратор
        else:
            raise permissions.PermissionDenied("У вас нет прав для удаления этого комментария.")  # Ошибка доступа
