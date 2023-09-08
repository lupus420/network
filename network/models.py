from django.contrib.auth.models import AbstractUser
from django.db import models

class Follow(models.Model):
    # follower follow the followed person
    follower = models.ForeignKey("User", on_delete=models.CASCADE, related_name="followed_by")
    followed = models.ForeignKey("User", on_delete=models.CASCADE, related_name="follower_of")
    date_followed = models.DateTimeField(auto_now_add=True)

    def serialize(self):
        return {
            "follower": self.follower.username,
            "followed": self.followed.username,
            "date_followed": self.date_followed.strftime("%b %d %Y, %I:%M %p"),
        }


class User(AbstractUser):
    # no need of adding 'following' because the Follow model
    # already hasa field 'follower' which is a User object
    # following = models.ManyToManyField("self",through=Follow, symmetrical=False, related_name="followees", blank=True)

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            # people who user follows
            "following": [user.username for user in self.follower_of.all()],
            # people who follow user
            "followers": [user.username for user in self.followed_by.all()],
        }
    

class Comment(models.Model):
    body = models.CharField(max_length=500)
    author = models.ForeignKey("User", on_delete=models.CASCADE, related_name="comments")
    date_posted = models.DateTimeField(auto_now_add=True)
    likes = models.ForeignKey(User, on_delete=models.CASCADE, related_name="liked_comments", blank=True, null=True)

    def serialize(self):
        return {
            "id": self.id,
            "body": self.body,
            "author": self.author.username,
            "date_posted": self.date_posted.strftime("%b %d %Y, %I:%M %p"),
            "likes_nr": self.likes.count(),
        }

class Post(models.Model):
    body = models.CharField(max_length=1000)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    comments = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="post_comments", blank=True, null=True)
    date_posted = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name="liked_posts", blank=True)

    def serialize(self):
        if self.comments:
            comments = [comment.serialize() for comment in self.comments.all()]
        else:
            comments = None
        if self.likes:
            likes_nr = self.likes.count()
        else:
            likes_nr = 0
        return {
            "id":           self.id,
            "body":         self.body,
            "author": {
                "username":     self.author.username,
                "id":       self.author.id,},
            "comments":     comments,
            "date_posted":  self.date_posted.strftime("%b %d %Y, %I:%M %p"),
            "likes_nr":     likes_nr,
            "likes":        [user.id for user in self.likes.all()],
        }