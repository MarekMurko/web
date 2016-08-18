#Indexes for haystack elasticsearch
from django.conf import settings

from haystack import indexes
from wiki.models import Article


class ArticleIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    modified = indexes.DateTimeField(model_attr='modified')
    title = indexes.CharField(model_attr='current_revision__title')
    content = indexes.CharField(model_attr='current_revision__content')
    deleted = indexes.BooleanField(model_attr='current_revision__deleted')
    locked = indexes.BooleanField(model_attr='current_revision__locked')
    urlpath = indexes.CharField(model_attr='get_absolute_url')
    id = indexes.IntegerField(model_attr='id')

    def get_model(self):
        return Article

    def prepare_urlpath(self, object):
        return object.get_absolute_url()

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(urlpath__site_id=settings.SITE_ID)
