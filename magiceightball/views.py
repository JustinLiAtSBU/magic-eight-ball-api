import re
import pycountry
from random import randint
from distutils.command.build import build
from django.db.models import Q
from django.shortcuts import render
from django.http.response import JsonResponse
from django.http import HttpResponse
from rest_framework.parsers import JSONParser
from rest_framework import status
from magiceightball.models import MotionPicture
from magiceightball.fuzzy_match import genre_match
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
    movies = MotionPicture.objects.filter(build_query(request) & Q(type='movie')).order_by('-rating')
    movies = filtered_by_genres(movies, request.GET.get('genres'))
    size = size if size < len(movies) and size > 0 else len(movies)
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
    movies = filtered_by_genres(movies, request.GET.get('genres'))
    size = size if size < len(movies) and size > 0 else len(movies)
    movie = movies[randint(0, size - 1)]
    movie_serializer = MotionPictureSerializer(movie)
    return JsonResponse(movie_serializer.data, safe=False)


@api_view(['GET', 'POST', 'DELETE'])
def tv_show_list(request):
    size = int(request.GET.get('size', 0))
    tv_shows = MotionPicture.objects.filter(build_query(request) & Q(type='tvSeries')).order_by('-rating')
    tv_shows = filtered_by_genres(tv_shows, request.GET.get('genres'))
    size = size if size < len(tv_shows) and size > 0 else len(tv_shows)
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
    tv_shows = filtered_by_genres(tv_shows, request.GET.get('genres'))
    size = size if size < len(tv_shows) and size > 0 else len(tv_shows)
    tv_show = tv_shows[randint(0, size - 1)]
    tv_show_serializer = MotionPictureSerializer(tv_show)
    return JsonResponse(tv_show_serializer.data, safe=False)


def build_query(request):
    query_result = Q()
    for key, value in request.GET.items():
        min_field = re.findall('[A-Z][^A-Z]*', key)
        if min_field:
            min_field = min_field[0].lower()
            if min_field == 'rating':
                query_result &= Q(rating__gte=value)
            elif min_field == 'year':
                query_result &= Q(year__gte=value)
            elif min_field == 'runtime':
                query_result &= Q(runtime__gte=value)
        else:
            if key == 'country':
                country = pycountry.countries.get(alpha_2=value)
                country_name = country.name
                if hasattr(country, 'common_name'):
                    country_name = country.common_name
                query_result &= Q(country=country_name)
    return query_result


def filtered_by_genres(motion_pictures, genres):
    if genres:
        genres = set([i.strip().upper() for i in genres.split(',')])
        genres = genre_match(genres)
        tconsts_to_remove = []
        for motion_picture in motion_pictures:
            motion_picture_genres = [i.strip().upper() for i in motion_picture.genres.split(',')]
            if genres.issubset(motion_picture_genres) is False:
                tconsts_to_remove.append(motion_picture.tconst)
        motion_pictures = motion_pictures.exclude(tconst__in=tconsts_to_remove)
    return motion_pictures