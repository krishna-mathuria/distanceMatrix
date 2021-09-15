from rest_framework.response import Response
from django.shortcuts import render
from rest_framework import status,generics
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from .models import History
from .forms import FileForm
import requests
from django.db.models import Q

# Create your views here.
API_KEY = 'cwG5DvwzcCiciFDRjn8IclxV8pRbGzWx'

# class getres(generics.ListAPIView):
#     serializer_class = Query
#     def get(self, request, *args, **kwargs):
#         to = kwargs.get('to')
#         fro = kwargs.get('from')
#         try:
#             distobj = History.objects.get(Q(origin=to,destination=fro) | Q(origin=fro,destination=to))
#             serializer = Dist(distobj)
#             return Response(serializer.data)
#         except:
#             params = {"from": fro, "to": to,"key":API_KEY}
#             res = requests.get('http://www.mapquestapi.com/directions/v2/route?',params=params)
#             res = res.json()
#             try:
#                 dist =  res['route']['distance']*1.615
#                 dist = "{:.2f}".format(dist) + " km"
#                 obj = History(origin = to,destination = fro,dist = dist)
#                 obj.save()
#                 serializer = Dist(obj)
#                 return Response(serializer.data)
#             except:
#                 return Response({"error": "Please enter valid values"}, status=status.HTTP_400_BAD_REQUEST)
#         return Response({"error": "Please enter valid values"}, status=status.HTTP_400_BAD_REQUEST)

def search(request):
    form = FileForm()
    if request.GET.get('origin'):
        to = request.GET.get('origin')
        fro = request.GET.get('destination')
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
                return render(request,'first.html',{'error': 'Please Enter Valid Entries.'})
        return render(request,'first.html',{'dist':dist,'Origin': to,'Destination':fro,'form': form})
    else:
        return render(request, 'second.html',{'form': form})


# @api_view(('GET',))
# def get_dist(request):
#     if request.method == "GET":
#         to = request.GET.get('origin')
#         fro = request.GET.get('destination')
#         key = API_KEY
#         try:
#             distobj = History.objects.get(Q(origin=to,destination=fro) | Q(origin=fro,destination=to)) 
#             dist = distobj.dist 
#         except:
#             params = {"from": fro, "to": to,"key":key}
#             res = requests.get('http://www.mapquestapi.com/directions/v2/route?',params=params)
#             res = res.json()
#             try:
#                 dist =  res['route']['distance']*1.615
#                 dist = "{:.2f}".format(dist) + " km"
#                 obj = History(origin = to,destination = fro,dist = dist)
#                 obj.save()
#             except:
#                 return render(request,'first.html',{'error': 'Please Enter Valid Entries.'})
#         return render(request,'first.html',{'dist':dist,'Origin': to,'Destination':fro})
#     else:
#         return Response({"error": "Method not allowed"}, status=status.HTTP_400_BAD_REQUEST)
