from .views import BookList
from rest_framework import routers
from .views import BookViewSet

router = routers.DefaultRouter()
router.register(r'books', BookViewSet, basename='book')
urlpatterns = [
    path("api/books", BookList.as_view(), name="book_list_create"),
    path('', include(router.urls))
]