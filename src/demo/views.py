from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, QueryDict
from django.template.loader import render_to_string



# Create your views here.
def base(request):
    return render(request, 'demo/base.html')

def render_response(request):
    print(request.method)
    print(request.GET)
    print(request.POST)
    print(QueryDict(request.body))
    data = dict()
    template_name = 'demo/demo.html'
    context = {'data': 'Some data from the server'}
    return render(request, template_name, context)

def json_response(request):
    print(request.method)
    print(request.GET)
    print(request.POST)
    print(QueryDict(request.body))
    data = dict()
    template_name = 'demo/demo.html'
    context = {'data': 'Some data from the server'}
    data['html'] = render_to_string(template_name, context, request=request) # render_to_string(template_name, context)
    data['data'] = context.get('data')
    return JsonResponse(data)

def form_request(request, something):
    print(something)
    print(request.method)
    print(request.GET)
    print(request.POST)
    print(QueryDict(request.body))
    data = dict()
    template_name = 'demo/demo.html'
    context = {'data': something}
    data['html'] = render_to_string(template_name, context, request=request) # render_to_string(template_name, context)
    data['data'] = context.get('data')
    return JsonResponse(data)