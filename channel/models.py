# account = users
from django.db import models
from accounts.models import User  # assuming you have a custom User model

class Channel(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_channels')
    subscribers = models.ManyToManyField(User, related_name='subscribed_channels', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def subscriber_count(self):
        return self.subscribers.count()

    def __str__(self):
        return self.name
