#import django_filters
from django_filters import FilterSet, DateFilter, DateFromToRangeFilter, CharFilter
from .models import Post



class NewsFilter(FilterSet):
    post_created = DateFromToRangeFilter()
    #post_header = CharFilter()
    #id_author__id_user__username = CharFilter()
    class Meta:
        model = Post
        fields = {
            'post_created': [],
            'post_header': ['icontains'],
            'id_author__id_user__username': ['icontains'],

        }

