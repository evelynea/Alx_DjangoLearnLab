from django.urls import path, include
from .views import BookList

from rest_framework import routers
from .views import BookViewSet
from rest_framework.authtoken.views import obtain_auth_token

router = routers.DefaultRouter()
router.register(r'books', BookViewSet, basename='book')
urlpatterns = [
    path("api/books", BookList.as_view(), name="book_list_create"),
    path('', include(router.urls)),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth')
]