from rest_framework.response import Response
from django.shortcuts import render
from rest_framework import status,generics
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.views import APIView
from .models import History
from .forms import FileForm
import requests
from django.db.models import Q

# Create your views here.
API_KEY = 'cwG5DvwzcCiciFDRjn8IclxV8pRbGzWx'

@api_view(('GET',))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def search(request):
    form = FileForm()
    if request.GET.get('origin'):
        try:
            to = request.GET.get('origin')
            fro = request.GET.get('destination')
        except:
            return Response({"error": "Please enter valid values"}, status=status.HTTP_400_BAD_REQUEST)
        key = API_KEY
        try:
            distobj = History.objects.get(Q(origin=to,destination=fro) | Q(origin=fro,destination=to)) 
            dist = distobj.dist 
        except:
            params = {"from": fro, "to": to,"key":key}
            res = requests.get('http://www.mapquestapi.com/directions/v2/route?',params=params)
            res = res.json()
            try:
                dist =  res['route']['distance']*1.615
                dist = "{:.2f}".format(dist) + " km"
                obj = History(origin = to,destination = fro,dist = dist)
                obj.save()
            except:
                return Response({"error": "Please enter valid values",'form': form}, status=status.HTTP_400_BAD_REQUEST, template_name='second.html')
        return render(request,'first.html',{'dist':dist,'Origin': to,'Destination':fro,'form': form})
    else:
        return render(request, 'second.html',{'form': form})
