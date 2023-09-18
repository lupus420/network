from django.test import TestCase, Client
from django.urls import reverse
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from json import loads
from .models import User, Post, Comment, Follow
# from django.views.decorators.csrf import csrf_exempt
from selenium import webdriver
import os
import pathlib
import unittest
import json

# Create your tests here.
from django.test import Client

class NetworkTestCase(TestCase):
    def setUp(self):
        # Create a user
        self.user1 = User.objects.create_user(username="user1",
                                         email="user1@email.com",
                                         password="Test12345")
        self.user2 = User.objects.create_user(username="user2",
                                         email="user2@email.com",
                                         password="Test12345")
        # Create a post
        self.post1 = Post.objects.create(body="Test post1",
                                        author=self.user1)
        # Create a comment
        self.comment = Comment.objects.create(body="Test comment",
                                              author=self.user1,
                                              parent_post=self.post1)
        
    def test_index(self):
        # Check that index page is accessible
        c = Client()
        response = c.get(reverse("index"))
        self.assertEqual(response.status_code, 200)


    # Check if users from setUp match the users from the database
    def check_users(self):
        users = User.objects.all()
        self.assertEqual(users, [self.user1, self.user2])


    def test_raw_login(self):
        c = Client()
        logged_in = c.login(username="user1", password="Test12345")
        self.assertTrue(logged_in)


    def test_login(self):
        c = Client()
        # Check that login page redirects to index page after login
        response = c.post(reverse("login"), {"username": "user1", "password": "Test12345"})
        # If user is logged in successfully, the response should be a redirect
        self.assertEqual(response.status_code, 302)


    def test_logout(self):
        c = Client()
        # Login first
        c.post(reverse("login"), {"username": "user1", "password": "Test12345"})
        # Check if logout page is accessible
        response = c.get(reverse("logout"))
        self.assertEqual(response.status_code, 302)


    def test_comment(self):
        # Check that comment page is accessible
        c = Client()
        # Pass the post_id as a query parameter
        response = c.get(reverse("get_comments") + "?post_id=" + str(self.post1.id))
        # Get the comments from the response
        comments = loads(response.content)
        # Check that the comment is in the comments list
        self.assertIn(self.comment.serialize(), comments)

### SELENIUM TESTS ###
    def test_title(self):
        # Check that title is "Social Network"
        driver = webdriver.Firefox()
        driver.get("http://127.0.0.1:8000")
        assert driver.title in "Social Network"
        driver.quit()
