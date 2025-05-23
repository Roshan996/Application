from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, permissions
from .models import Channel
from .serializers import ChannelSerializer

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from .permissions import IsOwnerOrReadOnly

class ChannelViewSet(viewsets.ModelViewSet):
    queryset = Channel.objects.all()
    serializer_class = ChannelSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

        
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def subscribe(self, request, pk=None):
        channel = self.get_object()
        user = request.user
        if user in channel.subscribers.all():
            return Response({'detail': 'Already subscribed'}, status=status.HTTP_400_BAD_REQUEST)
        channel.subscribers.add(user)
        return Response({'detail': 'Subscribed successfully'})

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def unsubscribe(self, request, pk=None):
        channel = self.get_object()
        user = request.user
        if user not in channel.subscribers.all():
            return Response({'detail': 'Not subscribed'}, status=status.HTTP_400_BAD_REQUEST)
        channel.subscribers.remove(user)
        return Response({'detail': 'Unsubscribed successfully'})
