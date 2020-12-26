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
from .permissions import IsOwner
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
    permission_classes = (IsOwner, IsAuthenticatedOrReadOnly,)
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['group', ]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    """Представление модели Comment."""
    serializer_class = CommentSerializer
    permission_classes = (IsOwner, IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        return post.comments


class GroupViewSet(CreateModelMixin,
                   ListModelMixin,
                   viewsets.GenericViewSet):
    """Представление модели Group."""
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class FollowViewSet(CreateModelMixin,
                    ListModelMixin,
                    viewsets.GenericViewSet):
    """Представление модели Follow."""
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = [IsFollowingFilterBackend]
    search_fields = ['=user__username', ]
    filterset_fields = ['following', ]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
