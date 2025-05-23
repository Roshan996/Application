from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    VideoUploadAPIView,
    VideoViewSet,
    LikeDislikeAPIView,
    CommentViewSet,
    CategoryViewSet,
    TagViewSet,
)

# Initialize the router
router = DefaultRouter()

# Register ViewSets with the router
router.register(r'videos', VideoViewSet, basename='video')
router.register(r'comments', CommentViewSet, basename='comment')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'tags', TagViewSet, basename='tag')

# Define URL patterns
urlpatterns = [
    # Upload a video (handled separately from ViewSet due to Cloudinary integration)
    path('upload/', VideoUploadAPIView.as_view(), name='video-upload'),

    # Like or dislike a video
    path('videos/<uuid:video_id>/vote/', LikeDislikeAPIView.as_view(), name='video-vote'),

    # Include all routes registered with the router
    path('', include(router.urls)),
]
