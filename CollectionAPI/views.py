from django.shortcuts import render
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.http import HttpResponse, JsonResponse, QueryDict
from . import views_helper as helper


@api_view(['GET'])
def get_request_count(request):
	response = helper.requests_count(request)
	return JsonResponse(response)

@api_view(['POST'])	
def reset_request_count(request):
	response = helper.requests_count(request)
	return JsonResponse(response)

@api_view(['POST'])	
@authentication_classes([])
@permission_classes([])
def register(request):
	response = helper.register(request)
	return JsonResponse(response)

@api_view(['GET'])
def movies(request):
	response = helper.movies()
	return JsonResponse(response)

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def collections(request, **kwargs):
	response = helper.collections(request, **kwargs)
	# return HttpResponse(response, content_type='application/json')
	return JsonResponse(response)