from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response
from rest_framework.views import APIView

from scrappers.tasks import start_scrapping


class ScrapperView(APIView):

    def get(self, request, format=None):
        start_scrapping()
        return Response({})
