from django.urls import path
from .views import google_authenticate, oauth2callback, list_reviews

urlpatterns = [
    path('auth/', google_authenticate, name='google_authenticate'),
    path('oauth2callback/', oauth2callback, name='oauth2callback'),
    path('reviews/', list_reviews, name='list_reviews'),
]
