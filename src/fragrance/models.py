from django.db import models
from django.core import serializers
from django.utils import timezone
from .managers import FragranceManager, URLManager

d1={'name':'a', 'brand':'a', 'size':100, 'gender':'man', 'type':'eau de toilette', 'seller':'Notino','url':'www.a.com', 'price':9, 'is_in_offer': False}
d2={'name':'a', 'brand':'a', 'size':100, 'gender':'man', 'type':'eau de toilette', 'seller':'Notino','url':'www.a.com', 'price':7, 'is_in_offer': True}
d3={'name':'a', 'brand':'a', 'size':100, 'gender':'man', 'type':'eau de toilette', 'seller':'Notino','url':'www.a.com', 'price':8, 'is_in_offer': False}
d4={'name':'a', 'brand':'a', 'size':100, 'gender':'man', 'type':'eau de toilette', 'seller':'Notino','url':'www.a.com', 'price':6, 'is_in_offer': True}

# Create your models here.
class Fragrance(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, verbose_name="name")
    brand = models.CharField(max_length=50, verbose_name="brand")
    size= models.IntegerField()
    GENDERS = [('man', 'man'), ('woman', 'woman'), ('unisex', 'unisex')]
    gender = models.CharField(
        max_length=6,
        choices=GENDERS,
        default='unisex',
        verbose_name='gender',
    )
    TYPES = [('eau de cologne', 'eau de cologne'), ('eau de toilette', 'eau de toilette'), ('eau de parfum', 'eau de parfum')]
    type = models.CharField(
        max_length=15,
        choices=TYPES,
        default='toilette',
        verbose_name='type',
    )
    url = models.URLField(verbose_name="url")
    seller  = models.CharField(max_length=50,verbose_name="seller")
    price = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    min_price = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    max_price = models.DecimalField(max_digits=5, decimal_places=2, default=0.0, null=True)
    min_offer_price = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    max_offer_price = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    is_in_offer = models.BooleanField(default=False)
    created_at = models.DateTimeField(editable=False, null=True, verbose_name="created at")
    updated_at = models.DateTimeField(editable=False, null=True, blank=True,
                                      verbose_name="updated at")
    checked_at = models.DateTimeField(editable=False, null=True, blank=True,
                                      verbose_name="checked at")

    class Meta:
        verbose_name='Fragrance'
        verbose_name_plural = 'Fragrances'
        ordering = ['seller','brand','name']

    objects = FragranceManager()


    def __str__(self):
        return f'{self.seller}: {self.brand} {self.name} Eau de {self.type} pour {self.gender} {self.price}{" in offer" if self.is_in_offer else ""} ({self.max_offer_price}-{self.min_offer_price}, {self.min_price}-{self.max_price})'

    def _update(self, *args, **kwargs) :

                if self.is_in_offer:
                    self.max_offer_price = self.price if self.price < self.max_offer_price else self.max_offer_price
                    self.min_offer_price = self.price if (self.max_price == 999 or self.price > self.min_offer_price) else self.min_offer_price
                else:
                    self.max_price = self.price if (self.max_price == 999 or self.price > self.max_price) else self.max_price
                    self.min_price = self.price if self.price < self.min_price else self.min_price

    def _init(self):
        self.max_price = self.price if not self.is_in_offer else 999
        self.min_price = self.price if not self.is_in_offer else 999
        self.max_offer_price = self.price
        self.min_offer_price = self.price

    def save(self, *args, **kwargs):
        now = timezone.localtime(timezone.now())
        if not self.created_at:
            print(f'Creating fragrance: {self.url}')
            self.created_at = now
            self._init()
        else:
            print(f'Updating fragrance: {self.url}')
            self.updated_at = now if now.date() > self.created_at.date() else None
            self._update()
        self.checked_at = now
        super(Fragrance, self).save(*args, **kwargs)

class classproperty(object):
    def __init__(self, fget):
        self.fget = fget
    def __get__(self, owner_self, owner_cls):
        return self.fget(owner_cls)


class URL (models.Model):
    url = models.URLField(verbose_name="url")
    domain = models.CharField(max_length=40)
    created_at = models.DateTimeField(editable=False, null=True, verbose_name="created at")

    class Meta():

        verbose_name = 'Url'
        verbose_name_plural = 'Urls'
        ordering = ['domain']

    objects = URLManager()

    @classproperty
    def urls(cls):
        return [url.url for url in URL.objects.all()]

    def __str__(self):
        return self.url

    def save(self, *args, **kwargs):
        now = timezone.localtime(timezone.now())
        if not self.created_at:
            self.created_at = now
            self.domain = self.url.replace('https://', '').replace('http://', '').replace('www.', '').split('/')[0]
            i = self.domain.rindex('.')
            self.domain = self.domain[0:i]
        super(URL, self).save(*args, **kwargs)





