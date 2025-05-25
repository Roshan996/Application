from rest_framework import viewsets, status, generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

from .models import Video, LikeDislike, Comment, Category, Tag
from .serializers import (
    VideoUploadSerializer, VideoSerializer,
    LikeDislikeSerializer, CommentSerializer,
    CategorySerializer, TagSerializer
)


# ---------------------------- Permissions ----------------------------

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.method in permissions.SAFE_METHODS or obj.uploaded_by == request.user


# ---------------------------- Video Upload ----------------------------

class VideoUploadAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = VideoUploadSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            video = serializer.save()
            return Response(VideoSerializer(video).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ---------------------------- Video ViewSet ----------------------------

class VideoViewSet(viewsets.ModelViewSet):
    queryset = Video.objects.filter(is_active=True).order_by('-uploaded_at')
    serializer_class = VideoSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_destroy(self, instance):
        # soft delete
        instance.is_active = False
        instance.save()


# ---------------------------- Like / Dislike ----------------------------

class LikeDislikeAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, video_id):
        video = get_object_or_404(Video, id=video_id)
        vote_value = request.data.get('vote')

        if vote_value not in ['1', '-1', 1, -1]:
            return Response({'detail': 'Vote must be 1 (like) or -1 (dislike)'}, status=400)

        vote, created = LikeDislike.objects.update_or_create(
            user=request.user, video=video,
            defaults={'vote': int(vote_value)}
        )

        return Response({'message': 'Vote recorded', 'vote': vote.vote})


# ---------------------------- Comments ----------------------------

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.filter(is_active=True).select_related('user', 'video')
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# ---------------------------- Category / Tag ----------------------------

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
