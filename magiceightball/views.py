from magiceightball.query_params import QUERY_PARAMS
from django.db.models import Q
from django.shortcuts import render
from django.http.response import JsonResponse
from django.http import HttpResponse
from rest_framework.parsers import JSONParser
from rest_framework import status

from magiceightball.models import MotionPicture
from magiceightball.serializers import MotionPictureSerializer
from rest_framework.decorators import api_view


@api_view(['GET'])
def health(self):
    return JsonResponse({'message': 'MagicEightBall API up and running'}, status=status.HTTP_200_OK)

@api_view(['GET'])
def motion_picture_list(request):
    print(request.GET)
    motion_pictures = MotionPicture.objects.all()
    motion_pictures_serializer = MotionPictureSerializer(motion_pictures, many=True)
    response = {
        'data': motion_pictures_serializer.data,
        'pagination': {
            'count': len(motion_pictures)
        }
    }
    return JsonResponse(response, safe=False) 


@api_view(['GET'])
def movie_list(request):
    size = int(request.GET.get('size', 0))
    movies = MotionPicture.objects.filter(type='movie').order_by('-rating')
    if size is not 0:
        movies = movies[:size]
    movies_serializer = MotionPictureSerializer(movies, many=True)
    response = {
        'data': movies_serializer.data,
        'pagination': {
            'count': len(movies)
        }
    }
    return JsonResponse(response, safe=False)


@api_view(['GET', 'POST', 'DELETE'])
def tv_show_list(request):
    print(request.GET)
    tv_shows = MotionPicture.objects.filter(type='tvSeries')
    tv_shows_serializer = MotionPictureSerializer(tv_shows, many=True)
    response = {
        'data': tv_shows_serializer.data,
        'pagination': {
            'count': len(tv_shows)
        }
    }
    return JsonResponse(response, safe=False)

@api_view(['GET'])
def motion_picture_detail(request):
    motion_picture_title = request.GET.get('title', '')
    try: 
        motion_picture = MotionPicture.objects.get(title=motion_picture_title)
        motion_picture_serializer = MotionPictureSerializer(motion_picture)
        response = {
            'data': motion_picture_serializer.data,
        }
        return JsonResponse(response, safe=False)
    except:
        return JsonResponse({'message': 'The motion picture does not exist'}, status=status.HTTP_404_NOT_FOUND) 


@api_view(['GET'])

def get_model_fields(model):
    return model._meta.fields

def query_movie():
    query = Q(year__gte=2000)
    query &= Q(type='movie')
    query &= Q(rating__gte=8)
    return {'type': 'movie'}


def build_query(request):
    query = Q()
    for key, value in request.GET.items():
        info = QUERY_PARAMS[key]
    
    # for key, value in QUERY_PARAMS.items():
    #     print(key, value)
