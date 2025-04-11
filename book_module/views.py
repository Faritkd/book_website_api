from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from django.shortcuts import get_object_or_404

from .models import Book, Author, Review
from .serializers import BookSerializer, AuthorSerializer, ReviewSerializer
from .permissions import IsAdminOrReviewOwnerReadOnly
from .pagination import CustomPageNumberPagination


# Concrete View Classes
class BookListView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    pagination_class = CustomPageNumberPagination



class BookDetailView(generics.RetrieveUpdateDestroyAPIView, APIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    


class AuthorListView(generics.ListCreateAPIView):
    permission_classes = [IsAdminUser]
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    pagination_class = CustomPageNumberPagination

    


class AuthorDetailView(generics.RetrieveAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    


class ReviewListView(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAdminOrReviewOwnerReadOnly]
    
    def get_queryset(self):
        pk = self.kwargs['pk']
        return Review.objects.filter(book=pk)
    
    def perform_create(self, serializer):
        book_id = self.kwargs['pk']
        book = Book.objects.get(pk=book_id)
        user = self.request.user
        
        if Review.objects.filter(book=book, user=user).exists():
            raise ValidationError('you have already reviewed this book. you cannot write more reviews!!')
        else:
            serializer.save(book=book, user=user)
    


class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAdminOrReviewOwnerReadOnly]
    
    

# using viewsets
# class BookViewSet(viewsets.ViewSet):
#     def list(self, request):
#         queryset = Book.objects.all()
#         serializer = BookSerializer(queryset, many=True)
#         return Response(serializer.data)
    
#     def retrieve(self, request, pk=None):
#         queryset = Book.objects.all()
#         book = get_object_or_404(queryset, pk=pk)
#         serializer = BookSerializer(book)
#         return Response(serializer.data)


# Using Mixins and GenericAPIView
# class BookListView(mixins.ListModelMixin, generics.GenericAPIView):
#     queryset = Book.objects.all()
#     serializer_class = BookSerializer
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)
    
    
# class AuthorListView(mixins.ListModelMixin, generics.GenericAPIView):
#     queryset = Author.objects.all()
#     serializer_class = AuthorSerializer
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs) 



# using the basic APIView
# class BookListView(APIView):
#     def get(self, request):
#         books = Book.objects.all()
#         serializer = BookSerializer(books, many=True)
#         return Response(serializer.data)
    
    
# class AuthorView(APIView):
#     def get(self, request):
#         authors = Author.objects.all()
#         serializer = AuthorSerializer(authors, many=True)
#         return Response(serializer.data)
