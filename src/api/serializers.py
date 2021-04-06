from rest_framework import serializers
from fragrance.models import Fragrance, URL

class FragranceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fragrance
        #fields="__all__"
        exclude=['min_price', 'max_price', 'min_offer_price', 'max_offer_price']
        #read_only_fields=['name', 'brand']

class URLSerializer(serializers.ModelSerializer):
    class Meta:
        model = URL
        fields=['url']

