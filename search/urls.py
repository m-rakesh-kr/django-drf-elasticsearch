
from django.urls import path
from search.views import SearchArticles, SearchCategories, SearchUsers, FilterArticles

urlpatterns = [
    path('user/<str:query>/', SearchUsers.as_view()),
    path('category/<str:query>/', SearchCategories.as_view()),
    path('article/<str:query>/', SearchArticles.as_view()),
    path('filter/articles/<str:query>/', FilterArticles.as_view(), name='filter_articles'),
]

