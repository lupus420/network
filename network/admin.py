from django.contrib import admin

# Register your models here.
from .models import User, Post, Comment, Follow

# Show table of follows in admin page
class FollowAdmin(admin.ModelAdmin):
    list_display = ("follower", "followed", "date_followed")

admin.site.register(User)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Follow, FollowAdmin)

