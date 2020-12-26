from rest_framework.filters import BaseFilterBackend


class IsFollowingFilterBackend(BaseFilterBackend):
    """Фильтрация подписчиков пользователя."""

    def filter_queryset(self, request, queryset, view):
        if 'search' in request.query_params:
            return queryset.filter(following=request.user,
                                   user__username=request.query_params[
                                       'search'])
        return queryset.filter(
            following=request.user)
