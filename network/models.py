from django.contrib.auth.models import AbstractUser
from django.db import models
from django.forms import ValidationError


class User(AbstractUser):

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            # people who user follows
            "following":[follow.followed.username for follow in self.followed_by.all()] if self.followed_by else [],
            # people who follow user
            "followers": [follow.follower.username for follow in self.following.all()] if self.following else [],
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

    def like_count(self):
        return self.likes.count()
    
    def serialize(self):
        if self.comments:
            comments = [comment.serialize() for comment in self.comments.all()]
        else:
            comments = None
        if self.likes:
            likes_nr = self.like_count()
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
    

class Follow(models.Model):
    # follower follow the followed person
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")
    followed = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followed_by")
    date_followed = models.DateTimeField(auto_now_add=True)
    
    def validate_follow(self):
        if self.follower == self.followed:
            raise ValidationError("You can't follow yourself.")
        return True

    def save(self, *args, **kwargs):
        if not self.validate_follow():
            # raise error
            raise ValidationError("Invalid follow.")
        super().save(*args, **kwargs)
    

    def serialize(self):
        return {
            "follower": self.follower,
            "followed": self.followed,
            "date_followed": self.date_followed.strftime("%b %d %Y, %I:%M %p"),
        }
    
    
    # add only unique follows
    class Meta:
        ordering = ["-date_followed"]
        constraints = [
            models.UniqueConstraint(fields=["follower", "followed"], name="unique_follow"),
        ]
        # another way to make unique follow validation
        # unique_together = ("follower", "followed")

