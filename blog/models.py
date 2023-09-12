from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=32)
    description = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return f'{self.name}'


ARTICLE_TYPE_UNSPECIFIED = 'UN'
ARTICLE_TYPE_TUTORIAL = 'TU'
ARTICLE_TYPE_RESEARCH = 'RS'
ARTICLE_TYPE_REVIEW = 'RW'

ARTICLE_TYPES = [
    (ARTICLE_TYPE_UNSPECIFIED, 'Unspecified'),
    (ARTICLE_TYPE_TUTORIAL, 'Tutorial'),
    (ARTICLE_TYPE_RESEARCH, 'Research'),
    (ARTICLE_TYPE_REVIEW, 'Review'),
]


class Article(models.Model):
    title = models.CharField(max_length=256)
    author = models.ForeignKey(to=User, on_delete=models.CASCADE)
    type = models.CharField(max_length=2, choices=ARTICLE_TYPES, default='UN')
    categories = models.ManyToManyField(to=Category, blank=True, related_name='articles')
    content = models.TextField()
    created_datetime = models.DateTimeField(auto_now_add=True)
    updated_datetime = models.DateTimeField(auto_now=True)

    def type_to_string(self):
        if self.type == 'UN':
            return 'Unspecified'
        elif self.type == 'TU':
            return 'Tutorial'
        elif self.type == 'RS':
            return 'Research'
        elif self.type == 'RW':
            return 'Review'

    def __str__(self):
        return f'{self.author}: {self.title} ({self.created_datetime.date()})'
