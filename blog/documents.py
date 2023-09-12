"""
    In this, I have used elasticsearch_dsl Library
    Instead of elasticsearch lib for Indexing of documents.
"""

from django.contrib.auth.models import User
from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from blog.models import Category, Article


@registry.register_document
class UserDocument(Document):
    class Index:
        name = 'users'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0,
        }

    class Django:
        model = User
        fields = [
            'id',
            'first_name',
            'last_name',
            'username',
        ]


@registry.register_document
class CategoryDocument(Document):
    id = fields.IntegerField()

    class Index:
        name = 'categories'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0,
        }

    class Django:
        model = Category
        fields = [
            'name',
            'description',
        ]


@registry.register_document
class ArticleDocument(Document):
    # author = fields.NestedField(properties={
    #     'id': fields.IntegerField(),
    #     'first_name': fields.TextField(),
    #     'last_name': fields.TextField(),
    #     'username': fields.TextField(),
    # })
    # categories = fields.NestedField(properties={
    #     'id': fields.IntegerField(),
    #     'name': fields.TextField(),
    #     'description': fields.TextField(),
    # })

    author = fields.ObjectField(properties={
        'id': fields.IntegerField(),
        'first_name': fields.TextField(),
        'last_name': fields.TextField(),
        'username': fields.TextField(),
    })
    categories = fields.ObjectField(properties={
        'id': fields.IntegerField(),
        'name': fields.TextField(),
        'description': fields.TextField(),
    })
    type = fields.TextField(attr='type_to_string')

    class Index:
        name = 'articles'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0,
        }

    class Django:
        model = Article
        fields = [
            'title',
            'content',
            'created_datetime',
            'updated_datetime',
        ]


""" 
    In this, I have used elasticsearch Library 
    Instead of elasticsearch_dsl lib for Indexing of documents.
"""

# from django.contrib.auth.models import User
# from elasticsearch_dsl import Document, InnerDoc, Integer, Text
# from elasticsearch_dsl.connections import connections
#
# from blog.models import Category, Article
#
# # Connect to Elasticsearch
# connections.create_connection(hosts=['localhost'])
#
#
# # User Document
# class UserDocument(Document):
#     id = Integer()
#     first_name = Text()
#     last_name = Text()
#     username = Text()
#
#     class Index:
#         name = 'users'
#
#     class Meta:
#         model = User
#
#
# # Category Document
# class CategoryDocument(Document):
#     id = Integer()
#     name = Text()
#     description = Text()
#
#     class Index:
#         name = 'categories'
#
#     class Meta:
#         model = Category
#
#
# # Article Document
# class ArticleDocument(Document):
#     author = InnerDoc(properties={
#         'id': Integer(),
#         'first_name': Text(),
#         'last_name': Text(),
#         'username': Text(),
#     })
#     categories = InnerDoc(properties={
#         'id': Integer(),
#         'name': Text(),
#         'description': Text(),
#     })
#     type = Text()
#
#     title = Text()
#     content = Text()
#     created_datetime = Text()
#     updated_datetime = Text()
#
#     class Index:
#         name = 'articles'
#
#     class Meta:
#         model = Article
