# book_website_api
# 📚 Book Review API

This is a backend-only project built with Django and Django REST Framework (DRF). It allows users to browse books and reviews, and enables authenticated users to submit reviews. Admin users can create authors and books.

## 🚀 Features

- User authentication using Token Authentication
- Only admins can create authors and books
- All users can:
  - View the list of books and book details
  - View reviews for each book
  - Create a review (only once per book)
- Permissions and validation:
  - A user can only review a book once
  - Reviews are linked to both the user and the book
- API responses in JSON format


## 📦 Technologies Used

- Django
- Django REST Framework (DRF)
- Token Authentication
- SQLite (default, easy to switch to PostgreSQL)
- DRF testing with `APITestCase`


## 🔐 Permissions

| Action               | Permission         |
|----------------------|--------------------|
| Create author/book   | Admin only         |
| View books/reviews   | All users          |
| Post a review        | Authenticated users only (one per book) |


## 🧪 Testing

Tests are written using `APITestCase`:

- Normal users are restricted from creating authors and books
- Only authenticated users can create reviews
- Duplicate reviews by the same user on the same book are rejected
- Anonymous users can view lists and details but cannot post

To run tests:

```bash
python manage.py test
