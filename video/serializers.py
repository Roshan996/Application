import cloudinary.uploader
from rest_framework import serializers
from .models import Video, LikeDislike, Comment, Category, Tag
import cloudinary


# ---------------------------- Category & Tag ----------------------------

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']


# ---------------------------- Video Upload ----------------------------

class VideoUploadSerializer(serializers.Serializer):
    title = serializers.CharField()
    description = serializers.CharField(required=False, allow_blank=True)
    video_file = serializers.FileField()
    thumbnail_file = serializers.ImageField(required=False)
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), required=False)
    tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(), many=True, required=False)
    privacy = serializers.ChoiceField(choices=Video.PRIVACY_CHOICES, default=Video.PUBLIC)

    def create(self, validated_data):
        video_file = validated_data.pop('video_file')
        thumbnail_file = validated_data.pop('thumbnail_file', None)

        # Upload video to Cloudinary
        video_upload = cloudinary.uploader.upload_large(
            video_file,
            resource_type="video",
            chunk_size = 6000000,
        )

        # Upload thumbnail if present
        thumbnail_url = None
        if thumbnail_file:
            thumb_upload = cloudinary.uploader.upload(
                thumbnail_file,
                resource_type="image",
            )
            thumbnail_url = thumb_upload['secure_url']

        video = Video.objects.create(
            video_url=video_upload['secure_url'],
            thumbnail_url=thumbnail_url,
            uploaded_by=self.context['request'].user,
            **validated_data
        )

        # Handle tags if provided
        tags = self.initial_data.get('tags', [])
        video.tags.set(tags)

        return video


# ---------------------------- Video Display ----------------------------

class VideoSerializer(serializers.ModelSerializer):
    uploaded_by = serializers.StringRelatedField(read_only=True)
    category = CategorySerializer()
    tags = TagSerializer(many=True)
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Video
        fields = [
            'id', 'title', 'description', 'video_url', 'thumbnail_url',
            'duration', 'format', 'resolution',
            'uploaded_at', 'uploaded_by',
            'privacy', 'category', 'tags',
            'views', 'likes_count', 'dislikes_count',
            'comments_count',
        ]

    def get_comments_count(self, obj):
        return obj.comments.filter(is_active=True).count()


# ---------------------------- Like / Dislike ----------------------------

class LikeDislikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LikeDislike
        fields = ['user', 'video', 'vote', 'created_at']


# ---------------------------- Comment ----------------------------

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'user', 'video', 'text', 'created_at', 'parent', 'replies']

    def get_replies(self, obj):
        if obj.replies.exists():
            return CommentSerializer(obj.replies.filter(is_active=True), many=True).data
        return []
