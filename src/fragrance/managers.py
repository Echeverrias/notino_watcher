from django.db import models
from .queries import FragranceQuerySet, URLQuerySet

class FragranceManager(models.Manager):

    def get_queryset(self):
        return FragranceQuerySet(
            model=self.model,
            using=self._db,
            hints=self._hints
        )

    def in_offer(self):
        return self.get_queryset().in_offer()

    def cheapies(self):
        return self.get_queryset().cheapies()

    def not_cheapies(self):
        return self.get_queryset().not_cheapies()

    def cheap_offers(self):
        return self.get_queryset().cheap_offers()

    def not_cheap_offers(self):
        return self.get_queryset().not_cheap_offers()


class URLManager(models.Manager):

    def get_queryset(self):
        return URLQuerySet(
            model=self.model,
            using=self._db,
            hints=self._hints
        )

    def notino(self):
        return self.get_queryset().notino()