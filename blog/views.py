from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters

from blog.models import Category, Article
from blog.serializers import CategorySerializer, ArticleSerializer, UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['id', 'username', 'last_name']  # Filtering
    search_fields = ['id', "username", 'last_name']  # Searching
    ordering_fields = '__all__'  # Sorting


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['id', 'name']
    search_fields = ['articles__type', 'description', 'id', 'name']
    ordering_fields = '__all__'


class ArticleViewSet(viewsets.ModelViewSet):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['type', 'categories']
    search_fields = ['author__username', 'author__last_name', 'title', 'type', 'categories__name']
    ordering_fields = '__all__'
