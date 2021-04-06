from django.http import HttpResponse
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from fragrance.models import Fragrance, URL
from .serializers import FragranceSerializer, URLSerializer

class FragranceViewSet(viewsets.ModelViewSet):
    queryset = Fragrance.objects.all()
    serializer_class = FragranceSerializer

@api_view(['GET', 'DELETE'])
def fragrance_element(request, pk):
    try:
        fragrance = Fragrance.objects.get(pk=pk)
        url = URL.objects.get(url=fragrance.url)
    except:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = FragranceSerializer(fragrance)
        return Response(serializer.data)

    elif request.method == 'DELETE':
        fragrance.delete()
        url.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
def fragrance_collection(request):
    fragrances = Fragrance.objects.all()
    if request.method == 'GET':
        serializer = FragranceSerializer(fragrances, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        print('POST')
        try:
            data = request.data
            fserializer = FragranceSerializer(data=data)
            if fserializer.is_valid():
                fserializer.save()
                urlSerializer = URLSerializer(data={'url': data['url']})
                if urlSerializer.is_valid():
                    urlSerializer.save()
                return Response(fserializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
        return Response(fserializer.errors, status=status.HTTP_400_BAD_REQUEST)