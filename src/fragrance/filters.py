from django.utils.translation import ugettext_lazy as _
import django_filters
from .models import Fragrance, URL
from django.db.models import Q, F
from datetime import date
from django import forms
import logging
logging.getLogger().setLevel(logging.INFO)

MONTHS = {
    1:_('Enero'), 2:_('Febrero'), 3:_('Marzo'), 4:_('Abril'),
    5:_('Mayo'), 6:_('Junio'), 7:_('Julio'), 8:_('Agosto'),
    9:_('Septiembre'), 10:_('Octubre'), 11:_('Noviembre'), 12:_('Diciembre')
}

class FragranceFilter(django_filters.FilterSet):

    class Meta:
        model = Fragrance
        fields = ['name_or_brand', 'price', 'is_in_offer']

    name_or_brand = django_filters.CharFilter(method='search_text', label='Search name or brand')
    price = django_filters.NumberFilter(lookup_expr='lte', label='Maximum price')
    cheapies = django_filters.BooleanFilter(method='search_cheapies', label='Cheapies')
    cheap_offers = django_filters.BooleanFilter(method='search_cheap_offers', label='Cheap offers')


    @property
    def qs(self):
        parent_qs = super(FragranceFilter, self).qs
        return parent_qs.filter(url__in=URL.urls)

    def search_cheapies(self, queryset, field_name, *args, **kwargs):
        if args[0]:
            return queryset.cheapies()
        else:
            return queryset.not_cheapies()

    def search_cheap_offers(self, queryset, field_name, *args, **kwargs):
        if args[0]:
            return queryset.cheap_offers()
        else:
            return queryset.not_cheap_offers()

    def search_text(self, queryset, field_name, *args, **kwargs):
        try:
            if args:
                qs = queryset.filter(Q(name__icontains=args[0])
                                     | Q(brand__icontains=args[0])
                                    )
                qs = qs.distinct()
                return qs
        except Exception as e:
            logging.exception("Error in search_text")
            return Fragrance.objects.none()
        return queryset