from rest_framework import serializers

from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueTogetherValidator

from .models import Group, Post, Comment, Follow


class PostSerializer(serializers.ModelSerializer):
    """Сериализатор модели Post."""
    author = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field='username',
    )

    class Meta:
        exclude = ('group',)
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор модели Comment."""
    author = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field='username',
    )

    class Meta:
        fields = ('id', 'author', 'post', 'text', 'created')
        model = Comment


class GroupSerializer(serializers.ModelSerializer):
    """Сериализатор модели Group."""

    class Meta:
        fields = ('id', 'title',)
        model = Group


class FollowSerializer(serializers.ModelSerializer):
    """Сериализатор модели Follow."""
    User = get_user_model()
    user = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )
    following = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all()
    )

    validators = [
        UniqueTogetherValidator(
            queryset=Follow.objects.all(),
            fields=['user', 'following']
        ),
    ]

    def validate_following(self, value):
        """Запрет подписки на самого себя."""
        if value == self.context['request'].user:
            raise serializers.ValidationError(
                'Нельзя подписаться на самого себя')
        return super().validate(value)

    class Meta:
        fields = ('user', 'following',)
        model = Follow
