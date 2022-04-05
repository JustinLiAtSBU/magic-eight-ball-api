from random import randint
import re
from distutils.command.build import build
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
def movie_list(request):
    size = int(request.GET.get('size', 0))
    movies = MotionPicture.objects.filter(type='movie').order_by('-rating')
    if size != 0:
        movies = movies[:size]
    movies_serializer = MotionPictureSerializer(movies, many=True)
    response = {
        'data': movies_serializer.data,
        'pagination': {
            'count': len(movies)
        }
    }
    return JsonResponse(response, safe=False)


@api_view(['GET'])
def random_movie(request):
    size = int(request.GET.get('size', 0))
    movies = MotionPicture.objects.filter(build_query(request) & Q(type='movie')).order_by('-rating')
    if size != 0:
        movies = movies[:size]
    size = size if size < len(movies) else len(movies)
    movie = movies[randint(0, size - 1)]
    movie_serializer = MotionPictureSerializer(movie)
    return JsonResponse(movie_serializer.data, safe=False)


@api_view(['GET', 'POST', 'DELETE'])
def tv_show_list(request):
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
def random_tv_show(request):
    size = int(request.GET.get('size', 0))
    tv_shows = MotionPicture.objects.filter(build_query(request) & Q(type='tvSeries')).order_by('-rating')
    if size != 0:
        tv_shows = tv_shows[:size]
    size = size if size < len(tv_shows) else len(tv_shows)
    tv_show = tv_shows[randint(0, size - 1)]
    tv_show_serializer = MotionPictureSerializer(tv_show)
    return JsonResponse(tv_show_serializer.data, safe=False)


def build_query(request):
    query_result = Q()
    for key, value in request.GET.items():
        field = re.findall('[A-Z][^A-Z]*', key)
        if field:
            field = field[0].lower()
            condition = re.match('[a-z]+', key)[0]
            if field == 'rating':
                query_result &= Q(rating__gte=value)
            elif field == 'year':
                query_result &= Q(year__gte=value)
            elif field == 'runtime':
                query_result &= Q(runtime__gte=value)
    return query_result
