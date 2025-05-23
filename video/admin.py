from django.contrib import admin
from .models import Video,Category, Tag, LikeDislike

admin.site.register(Video)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(LikeDislike)