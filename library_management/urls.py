from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from books.views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='homepage'),
    path('category/<slug:category_slug>/', home, name='category_wise_book'),
    path('books/', include('books.urls')),
    path('authenticate/', include('users.urls')),
]
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)