from django.contrib import admin
from django.urls import path, include
from accounts import views as account_views

urlpatterns = [
    path('', account_views.home, name='home'),
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('', include('scheduling.urls')),
    path('', include('bookings.urls')),
]
