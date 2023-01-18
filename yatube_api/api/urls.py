from rest_framework.routers import DefaultRouter

from django.urls import include, path

from .views import PostViewSet, GroupViewSet, CommentViewSet


router = DefaultRouter()

router.register('posts', PostViewSet)
router.register('groups', GroupViewSet)
router.register(
    r'posts/(?P<post_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/', include('djoser.urls'),),
    path('v1/', include('djoser.urls.jwt')),
]
