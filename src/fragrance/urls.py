from django.urls import path
from django.views.generic.detail import DetailView
from django.conf import settings
from django.conf.urls.static import static
# from django.contrib.auth.decorators import login_required # login_required(DetailView.as_view(model=Fragrance))
from .views import FragranceListView, create_fragrance, delete_fragrance
from .models import Fragrance

urlpatterns = [
    path("", FragranceListView.as_view(), name='fragrance_list'),
    path("create/", create_fragrance, name='fragrance_create'),
    path("delete/<int:pk>/", delete_fragrance, name='fragrance_delete'),
    path("<int:pk>/", DetailView.as_view(model=Fragrance), name='fragrance_detail'),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)