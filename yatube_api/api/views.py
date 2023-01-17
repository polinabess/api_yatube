# from django.shortcuts import render

from rest_framework import viewsets
from posts.models import Post, Group
from .serializers import PostSerializer, GroupSerializer, CommentSerializer
from django.core import exceptions
from rest_framework import permissions
from django.shortcuts import get_object_or_404
from .permissions import AuthorOrReadOnly
from rest_framework.response import Response
from rest_framework import status


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticated, AuthorOrReadOnly)

    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save(author=self.request.user)
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise exceptions.PermissionDenied(
                "Изменение чужого контента запрещено!"
            )
        super(PostViewSet, self).perform_update(serializer)

    def deperform_destroy(self, serializer):
        if serializer.instance.author != self.request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        super(PostViewSet, self).deperform_destroy(serializer)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (AuthorOrReadOnly, permissions.IsAuthenticated)

    def get_post_id(self):
        return get_object_or_404(Post, self.kwargs.get("post_id"))

    def get_queryset(self):
        post = self.get_post_id()
        return Post.objects.filter(post=post)

    def get_queryset(self):
        post = self.get_post_id()
        return post.comments.all()

    def perform_create(self, serializer):
        post = self.get_post_id()
        serializer.save(author=self.request.user, post=post)

    def deperform_destroy(self, serializer):
        post = self.get_post_id()
        if post.author != self.request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        super(CommentViewSet, self).deperform_destroy(serializer)
