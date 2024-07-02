from django.contrib import admin
from .models import  Borrowing, Review, Book,Category

admin.site.register(Borrowing)
admin.site.register(Review)
admin.site.register(Book)
admin.site.register(Category)

