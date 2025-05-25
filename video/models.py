# videos

import uuid
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, db_index=True)

    def __str__(self):
        return self.name

class Video(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # scalable unique ID

    # Basic info
    title = models.CharField(max_length=255, db_index=True)
    description = models.TextField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True, db_index=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='videos')
    #updated_at = models.DateTimeField(auto_now=True)

    # Video files (URLs or paths to storage like S3)
    video_url = models.URLField()
    thumbnail_url = models.URLField(blank=True, null=True)

    # Video metadata
    duration = models.DurationField(null=True, blank=True)
    format = models.CharField(max_length=50, blank=True)  # e.g., mp4, webm
    resolution = models.CharField(max_length=20, blank=True)  # e.g., 1920x1080

    # Visibility / privacy
    PUBLIC = 'public'
    PRIVATE = 'private'
    UNLISTED = 'unlisted'
    PRIVACY_CHOICES = [(PUBLIC, 'Public'), (PRIVATE, 'Private'), (UNLISTED, 'Unlisted')]
    privacy = models.CharField(max_length=10, choices=PRIVACY_CHOICES, default=PUBLIC, db_index=True)

    # Categorization
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='videos')
    tags = models.ManyToManyField('Tag', blank=True, related_name='videos')

    # Usage stats (increment in an atomic way via DB or cache)
    views = models.PositiveBigIntegerField(default=0, db_index=True)
    likes_count = models.PositiveIntegerField(default=0)
    dislikes_count = models.PositiveIntegerField(default=0)

    # Soft deletion flag
    is_active = models.BooleanField(default=True, db_index=True)

    def __str__(self):
        return self.title

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True, db_index=True)

    def __str__(self):
        return self.name

class LikeDislike(models.Model):
    LIKE = 1
    DISLIKE = -1
    VOTE_CHOICES = [(LIKE, 'Like'), (DISLIKE, 'Dislike')]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='votes')
    vote = models.SmallIntegerField(choices=VOTE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'video')
        indexes = [
            models.Index(fields=['video', 'vote']),
        ]

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')

    is_active = models.BooleanField(default=True, db_index=True)

    def __str__(self):
        return f'Comment by {self.user.username} on {self.video.title}'
