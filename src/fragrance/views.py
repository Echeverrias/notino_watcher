from django.views.generic.list import ListView
from django.views.decorators.csrf import csrf_protect
import json
from django.shortcuts import render
#from django.contrib.auth.decorators import login_required
#from django.contrib.admin.views.decorators import staff_member_required
# from django.utils.decorators import method_decorator
from django.http import HttpResponse, QueryDict, JsonResponse
from django.core import serializers
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie

from django.conf import settings
import time
from django.template.loader import render_to_string
from .models import Fragrance, URL
from .filters import FragranceFilter
from .forms import URLForm
from .tasks import get_notino_fragrance_data_and_update_fragrances_db_task, save_urls_watched_to_json_task

CACHE_TTL = 180 #getattr(settings, 'CACHE_TTL', 900)
CACHE_KEY_PREFIX = getattr(settings, 'CACHE_KEY_PREFIX', 'redis')

#@method_decorator(login_required, name='dispatch')
@method_decorator(cache_page(CACHE_TTL, key_prefix='notino'), name='dispatch')
class FragranceListView(ListView):
    model = Fragrance
    context_object_name = 'fragrance_list'
    template_name = 'fragrance/query_form.html'
    ordering = ('brand', 'name')
    #paginate_by = 20

    def get_queryset(self, *args, **kwargs):
        qs = super(FragranceListView, self).get_queryset()
        self.fragrance_filtered_list = FragranceFilter(self.request.GET, qs)
        return self.fragrance_filtered_list.qs

    def get_context_data(self, **kwargs):
        context = super(FragranceListView, self).get_context_data(**kwargs)
        context['filter_form'] = self.fragrance_filtered_list.form
        return context


def create_fragrance(request):
    print('create_fragrance')
    if request.is_ajax() or request.method == 'POST':
        print('ajax/POST request')
        url = request.POST.get('url')
        form = URLForm(request.POST)
        if form.is_valid():
            print('valid form')
            instance = form.save(commit=False)
            instance.save()
            save_urls_watched_to_json_task.delay()
            task = get_notino_fragrance_data_and_update_fragrances_db_task.delay(url)
            qs = None
            count = 0
            while (not qs and count < 5):
                qs = Fragrance.objects.filter(url=url)
                count= count + 1
                time.sleep(1)
            if qs:
                string = serializers.serialize("json", qs)
                fragrances = json.loads(string)
                fragrance = fragrances[0].get('fields') # keys == ['model', 'pk', 'fields']
                fragrance.setdefault('pk', fragrances[0].get('pk'))
                data = {'message': 'The fragrance is been watched', 'fragrance':fragrance}
                return JsonResponse(data)
            else:
                return JsonResponse({'error': 'The fragrance has not been stored in the db'})
        else:
            return JsonResponse({'error':'URL incorrect or is already been watched'})
    else:
        return HttpResponse(None)


def delete_fragrance(request, pk=None):
    print('delete_fragrance')
    print(pk)
    if request.is_ajax():
        print('ajax or delete')
        if not pk:
            pk = QueryDict(request.body).get('pk')
        pk = int(pk)
        try:
            print(pk)
            fragrance = Fragrance.objects.get(pk=pk)
            print(fragrance)
            URL.objects.filter(url=fragrance.url).delete()
            save_urls_watched_to_json_task.delay()
            return JsonResponse({'message':'The fragrance has been unwatched'})
        except Exception as e:
            print(e)
            return JsonResponse({'error':'Some error has happened'})