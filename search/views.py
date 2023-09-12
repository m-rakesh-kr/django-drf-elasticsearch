"""
    In this, I have used elasticsearch_dsl Library
    Instead of elasticsearch lib for Constructing and Executing Queries.
"""
import abc

from django.http import HttpResponse
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from elasticsearch_dsl import Q
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.views import APIView

from blog.documents import ArticleDocument, UserDocument, CategoryDocument
from blog.serializers import ArticleSerializer, UserSerializer, CategorySerializer


class PaginatedElasticSearchAPIView(APIView, LimitOffsetPagination):
    serializer_class = None
    document_class = None

    @abc.abstractmethod
    def generate_q_expression(self, query):
        """This method should be overridden
        and return a Q() expression."""

    def get(self, request, query):
        try:
            q = self.generate_q_expression(query)
            print(q)
            search = self.document_class.search().query(q)
            response = search.execute()

            print(f'Found {response.hits.total.value} hit(s) for query: "{query}"')

            results = self.paginate_queryset(response, request, view=self)
            serializer = self.serializer_class(results, many=True)
            return self.get_paginated_response(serializer.data)
        except Exception as e:
            return HttpResponse(e, status=500)


# views
class SearchUsers(PaginatedElasticSearchAPIView):
    serializer_class = UserSerializer
    document_class = UserDocument

    def generate_q_expression(self, query):
        return Q('bool',
                 should=[
                     Q('match', username=query),
                     Q('match', first_name=query),
                     Q('match', last_name=query),
                 ], minimum_should_match=1)


class SearchCategories(PaginatedElasticSearchAPIView):
    serializer_class = CategorySerializer
    document_class = CategoryDocument

    def generate_q_expression(self, query):
        return Q(
            'multi_match', query=query,
            fields=[
                'name',
                'description',
            ], fuzziness='auto')


class SearchArticles(PaginatedElasticSearchAPIView):
    serializer_class = ArticleSerializer
    document_class = ArticleDocument

    def generate_q_expression(self, query):
        return Q(
            'multi_match', query=query,
            fields=[
                'title',
                'content',
                'auther.username',
                'categories.name'
            ], fuzziness='auto')


class FilterArticles(PaginatedElasticSearchAPIView):
    serializer_class = ArticleSerializer
    document_class = ArticleDocument

    def generate_q_expression(self, query):
        # Get filter parameters from request
        article_type = self.request.query_params.get('type')
        author_id = self.request.query_params.get('author')
        category_id = self.request.query_params.get('category')

        q = Q('multi_match', query=query, fields=['title', 'content', 'author.username', 'categories.name'],
              fuzziness='auto')

        if article_type:
            return Q('term', type=article_type)

        if author_id:
            return Q('nested', path='author', query=Q('term', **{'author.id': author_id}))

        if category_id:
            return Q('nested', path='categories', query=Q('term', **{'categories.id': category_id}))

        # Default query to match all documents if no filter conditions are specified
        return q


""" 
    In this, I have used elasticsearch Library 
    Instead of elasticsearch_dsl lib for Constructing and Executing Queries.
"""
# from elasticsearch import Elasticsearch
# from elasticsearch_dsl import Search
# from elasticsearch_dsl.query import Q
# from rest_framework.pagination import LimitOffsetPagination
# from rest_framework.response import Response
# from rest_framework.views import APIView
#
# from blog.serializers import ArticleSerializer, UserSerializer, CategorySerializer
# from blog.documents import ArticleDocument, UserDocument, CategoryDocument
#
#
# class PaginatedElasticSearchAPIView(APIView, LimitOffsetPagination):
#     serializer_class = None
#     document_class = None
#
#     def generate_q_expression(self, query):
#         """
#         This method should be overridden and return a Q() expression.
#         """
#         pass
#
#     def get(self, request, query):
#         try:
#             q = self.generate_q_expression(query)
#
#             # Create an Elasticsearch client
#             es = Elasticsearch()
#
#             # Create a search object
#             search = Search(using=es).query(q)
#
#             # Execute the search
#             response = search.execute()
#
#             print(f'Found {response.hits.total.value} hit(s) for query: "{query}"')
#
#             print(response)
#
#             results = self.paginate_queryset(response, request, view=self)
#             serializer = self.serializer_class(results, many=True)
#             return self.get_paginated_response(serializer.data)
#         except Exception as e:
#             return Response(str(e), status=500)
#
# class SearchUsers(PaginatedElasticSearchAPIView):
#     serializer_class = UserSerializer
#     document_class = UserDocument
#
#     def generate_q_expression(self, query):
#         return Q('bool',
#                  should=[
#                      Q('match', username=query),
#                      Q('match', first_name=query),
#                      Q('match', last_name=query),
#                  ], minimum_should_match=1)
#
#
# class SearchCategories(PaginatedElasticSearchAPIView):
#     serializer_class = CategorySerializer
#     document_class = CategoryDocument
#
#     def generate_q_expression(self, query):
#         return Q(
#             'multi_match', query=query,
#             fields=[
#                 'name',
#                 'description',
#             ], fuzziness='auto')
#
#
# class SearchArticles(PaginatedElasticSearchAPIView):
#     serializer_class = ArticleSerializer
#     document_class = ArticleDocument
#
#     def generate_q_expression(self, query):
#         return Q('multi_match', query=query, fields=['title', 'content', 'author.username', 'categories.name'],
#               fuzziness='auto')
#
#
