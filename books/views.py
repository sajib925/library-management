from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from .models import Book, Borrowing, Review, Category
from .forms import  ReviewForm
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from .models import Book, Borrowing
from .forms import ReviewForm
from users.models import Profile 
from django.utils import timezone



@login_required
def borrow_book(request, pk):
    book = Book.objects.get(id=pk)
    user_profile, created = Profile.objects.get_or_create(user=request.user, defaults={'balance': 0})
    
    if user_profile.balance >= book.borrowing_price:
        user_profile.balance -= book.borrowing_price
        user_profile.save()
        Borrowing.objects.create(user=request.user, book=book, price=book.borrowing_price)
        
        send_mail(
            'Book Borrowed',
            f'You have successfully borrowed the book: {book.title}',
            'from@example.com',
            [request.user.email],
            fail_silently=False,
        )
        return redirect('borrow-history')
    
    return render(request, 'borrow_book.html', {'book': book, 'error': 'Insufficient balance'})


@login_required
def return_book(request, pk):
    borrowing = get_object_or_404(Borrowing, id=pk)
    borrowing.returned_at = timezone.now()
    borrowing.save()

    user_profile = request.user.profile
    user_profile.balance += borrowing.price
    user_profile.save()

    send_mail(
        'Book Returned',
        f'You have successfully returned the book: {borrowing.book.title}',
        'from@example.com',
        [request.user.email],
        fail_silently=False,
    )
    return redirect('borrow-history')



@login_required
def borrow_history(request):
    borrowings = Borrowing.objects.filter(user=request.user)
    return render(request, 'borrow_history.html', {'borrowings': borrowings})

def home(request, category_slug=None):
    categories = Category.objects.all()
    books = Book.objects.all()
    if category_slug:
        category = Category.objects.get(slug=category_slug)
        books = books.filter(category=category) 
    return render(request, 'home.html', {'books': books, 'categories': categories})



@login_required
def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    borrowings = Borrowing.objects.filter(book=book, user=request.user, returned_at__isnull=False)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.book = book
            review.save()
            return redirect('book-detail', pk=book.pk)
    else:
        form = ReviewForm()
    reviews = Review.objects.filter(book=book)
    return render(request, 'book_detail.html', {'book': book, 'form': form, 'reviews': reviews, 'can_review': borrowings.exists()})

