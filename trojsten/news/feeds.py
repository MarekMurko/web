# coding: utf-8
from __future__ import unicode_literals
from django.contrib.syndication.views import Feed
from django.contrib.sites.models import get_current_site
from django.utils import feedgenerator
from django.utils.translation import ugettext_lazy

from trojsten.news.models import Entry


class NewsFeed(Feed):
    feed_type = feedgenerator.Atom1Feed
    link = "/"

    def get_object(self, request):
        return get_current_site(request)

    def title(self, obj):
        # Translators: original: %s: Novinky
        return ugettext_lazy("%s: News") % (obj.name,)

    def items(self, obj):
        return Entry.objects.filter(sites__id__exact=obj.pk)[:10]

    def item_link(self):
        return "/"

    def item_author_name(self, item):
        return item.author.username

    def item_pubdate(self, item):
        return item.pub_date

    def item_description(self, item):
        return item.rendered_text()
