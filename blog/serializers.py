from django.contrib.auth.models import User
from rest_framework import serializers
from blog.models import Article, Category


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ArticleSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    categories = CategorySerializer(many=True, read_only=True)

    class Meta:
        model = Article
        fields = '__all__'
        read_only_fields = ['author']  # Add this line

    # def create(self, validated_data):
    #     author_data = validated_data.pop('author')
    #     categories_data = validated_data.pop('categories')
    #
    #     # Check if the user already exists
    #     try:
    #         author = User.objects.get(username=author_data['username'])
    #     except User.DoesNotExist:
    #         # User doesn't exist, create a new one
    #         author = User.objects.create(**author_data)
    #
    #     article = Article.objects.create(author=author, **validated_data)
    #
    #     for category_data in categories_data:
    #         # Check if the category already exists
    #         try:
    #             category = Category.objects.get(name=category_data['name'])
    #         except Category.DoesNotExist:
    #             # Category doesn't exist, create a new one
    #             category = Category.objects.create(**category_data)
    #
    #         article.categories.add(category)
    #
    #     return article

    def update(self, instance, validated_data):
        # Exclude 'author' from the validated data to prevent updating it
        validated_data.pop('author', None)

        # Perform the update
        instance = super().update(instance, validated_data)

        return instance
