from django.urls import path
from django.views.generic.detail import DetailView
from django.conf import settings
from django.conf.urls.static import static
# from django.contrib.auth.decorators import login_required # login_required(DetailView.as_view(model=Fragrance))
from .views import json_response, render_response, base, form_request

urlpatterns = [
    path("", base, name='base'),
    path("form-request/<str:something>", form_request, name='form_request'),
    path("json-response/", json_response, name='json_response'),
    path("render-response/", render_response, name='render_response'),
]