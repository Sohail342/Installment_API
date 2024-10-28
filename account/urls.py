from django.urls import path
from .views import JWTLoginView

urlpatterns = [
    path('login/', JWTLoginView.as_view(), name='login'),
]
