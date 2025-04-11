from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# router = DefaultRouter()
# router.register(r'books', views.BookViewSet, basename='books')

urlpatterns = [
    # path('', include(router.urls)),
    path('books/', views.BookListView.as_view(), name='booklist'),
    path('books/<int:pk>/', views.BookDetailView.as_view(), name='book_detail'),
    path('authors/', views.AuthorListView.as_view(), name='authorlist'),
    path('authors/<int:pk>/', views.AuthorDetailView.as_view(), name='author_detail'),
    path('books/<int:pk>/reviews/', views.ReviewListView.as_view(), name='reviews'),
    path('reviews/<int:pk>/', views.ReviewDetailView.as_view(), name='review_detail'),
]
