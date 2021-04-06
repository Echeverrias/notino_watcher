from django.urls import include, path
from rest_framework import routers

from .views import FragranceViewSet, fragrance_element, fragrance_collection

router = routers.DefaultRouter()
router.register(r'fragrances', FragranceViewSet)

#router.register(r'fragrances/{pk}', fragrance_element, basename='Fragrance') # doesnt work with a function

urlpatterns = [
    path('', include(router.urls)),
    path(r'<int:pk>', fragrance_element, name='fragrance_element'),
    path(r'all', fragrance_collection, name='fragrance_collection'),
    path('api-auth', include('rest_framework.urls')),
]