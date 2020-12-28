from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly
)

from .filters import IsFollowingFilterBackend
from .models import Post, Group, Follow
from .permissions import IsAuthorOrReadOnly
from .serializers import (
    CommentSerializer,
    PostSerializer,
    GroupSerializer,
    FollowSerializer
)


class PostViewSet(viewsets.ModelViewSet):
    """Представление модели Post."""
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthorOrReadOnly, IsAuthenticatedOrReadOnly,)
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['group', ]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    """Представление модели Comment."""
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrReadOnly, IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        serializer.save(author=self.request.user, post=post)

    def get_queryset(self):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        return post.comments


class CreateListViewSet(CreateModelMixin,
                        ListModelMixin,
                        viewsets.GenericViewSet):
    """Набор микмисонов для создания и представления моделей."""
    pass


class GroupViewSet(CreateListViewSet):
    """Представление модели Group."""
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class FollowViewSet(CreateListViewSet):
    """Представление модели Follow."""
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = [IsFollowingFilterBackend]
    search_fields = ['=user__username', ]
    filterset_fields = ['following', ]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
