from django.urls import path
from . import views

urlpatterns = [
    path('books/<int:pk>/', views.book_detail, name='book-detail'),
    path('borrow/<int:pk>/', views.borrow_book, name='borrow-book'),
    path('borrow/history/', views.borrow_history, name='borrow-history'),
    path('return/<int:pk>/', views.return_book, name='return-book'),
]
