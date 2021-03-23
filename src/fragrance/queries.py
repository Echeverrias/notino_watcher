from django.db import models
#from django.db.models import Q, F

class FragranceQuerySet(models.QuerySet):

    def in_offer(self):
        return self.filter(is_in_offer=True)

    def cheapies(self):
        return self.filter(price__lte=21.99)

    def not_cheapies(self):
        return self.filter(price__gt=21.99)

    def cheap_offers(self):
        return self.filter(is_in_offer=True, price__lte=25.99)

    def not_cheap_offers(self):
        return self.filter(is_in_offer=True, price__gt=25.99)



class URLQuerySet(models.QuerySet):

    def notino(self):
        print('URLQueryset')
        return self.filter(url__contains='notino')