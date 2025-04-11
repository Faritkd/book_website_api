from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token

from . import serializers
from . import models


# only admin users can create authors. so normal users or unauthenticated users cannot create authors(HTTP_403_FORBIDDEN)
class AuthorTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="test",password="1qaz@WSX")
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
    
    
    def test_author(self):
        data = {
            "name": "authortest",
            "about_author": "test text",
        }
        
        response = self.client.post(reverse("authorlist"), data)
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)
        

class BookListTestCase(APITestCase):
    def test_book_list(self):
        response = self.client.get(reverse("booklist"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        

class BookDetailTestCase(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_superuser(username="test", password="1qaz@WSX")
        self.admin_token = Token.objects.create(user=self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATON="Token "+ self.admin_token.key)
        self.author = models.Author.objects.create(name="author", about_author="good author")
        self.book = models.Book.objects.create(title="testbook", summary="testsummary", author=self.author)
        
    def test_book_detail(self):
        response = self.client.get(reverse("book_detail", args=[self.book.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        
class ReviewTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="test2", password="1qaz@WSX")
        self.user_token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Token "+ self.user_token.key)
        self.author = models.Author.objects.create(name="author", about_author="good author")
        self.book = models.Book.objects.create(title="testbook", summary="testsummary", author=self.author)   
    
    def test_create_review(self):
        data = {
            "rating": 5,
            "review": "Excellent read!"
        }
        response = self.client.post(reverse("reviews", args = [self.book.id]), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    
    def test_review_detail(self):
        review = models.Review.objects.create(user=self.user, rating=4, review="good book", book=self.book)
        response = self.client.get(reverse("review_detail", args=[review.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    