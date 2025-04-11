from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.


class Author(models.Model):
    name = models.CharField(max_length=100)
    about_author = models.TextField(null=True)
    
    def __str__(self):
        return self.name
    
    
class Book(models.Model):
    title = models.CharField(max_length=200)
    summary = models.TextField()
    author = models.ForeignKey(Author, related_name='books', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title


class Review(models.Model):
    user = models.ForeignKey(User, related_name='reviews', on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    review = models.TextField()
    book = models.ForeignKey(Book, related_name='reviews', on_delete=models.CASCADE, null=True)
    
    class Meta:
        unique_together = ('user', 'book')
    
    def __str__(self):
        return f'user:{self.user} | rating:{self.rating} | book:{self.book.title}'