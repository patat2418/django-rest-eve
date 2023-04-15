from django import shortcuts
from django.shortcuts import get_object_or_404, render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request

from movies_rest_app.models import *
from movies_rest_app.seiralizer import *
# Create your views here.

@api_view(['GET', 'POST'])
def get_movies(request:Request):
    if request.method == 'GET':
        query_params = request.query_params
        movies_qs = Movie.objects.all()
        
        if 'name' in query_params:
            movies_qs = movies_qs.filter(name__iexact=query_params['name'])
        if 'duration_from' in query_params:
            movies_qs = movies_qs.filter(duration_in_min__gte=query_params['duration_from'])
        if 'duration_to' in query_params:
            movies_qs = movies_qs.filter(duration_in_min__lte=query_params['duration_to'])
        if 'description' in query_params:
            movies_qs = movies_qs.filter(description__icontines=query_params['description'])
        # serializer = MovieSerializer(instance=movies_qs, many=True)
        serializer = MovieSerializer2(instance=movies_qs, many=True)
        return Response(serializer.data)
    else:
        serializer = MovieSerializer2(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(status=201,data=serializer.data)     

@api_view(['GET'])
def get_actors(request:Request):
    qs = Actor.objects.all()
    serializer = ActorSerializer1(instance=qs, many=True)
    return Response(serializer.data)

@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def get_movie(request:Request,movie_id:int):
    movie = shortcuts.get_object_or_404(Movie,id=movie_id)
    if request.method == 'GET':    
        serializer = MovieDetailesSerializer(instance=movie, many=False)
        return Response(serializer.data)
    elif request.method in ['PUT','PATCH']:
        serializer = MovieSerializer2(instance=movie, data=request.data, partial=(request.method == 'PATCH'),context={'request':request})
        if serializer.is_valid(raise_exception=True):
            update_movie =serializer.save()
            return Response (MovieDetailesSerializer(instance=update_movie).data)
    else:
        movie.delete()
        return Response(status=200)


@api_view(['GET', 'POST'])
def get_movie_actors(request:Request,movie_id:int):
    
    if request.method == 'GET':
        movie = shortcuts.get_object_or_404(Movie,id=movie_id)
        qs =movie.movieactor_set.all()
        query_params = request.query_params  
        if 'main_roles' in query_params:
            qs = qs.filter(main_role=True)
        if 'salary_from' in query_params:
            qs = qs.filter(salary__gte=query_params['salary_from'])
        if 'salary_to' in query_params:
            qs = qs.filter(salary__lte=query_params['salary_to'])
        serializer = MovieActorsSerializer(instance=qs, many=True)
        # serializer = AddCastSerializer(instance=qs, many=True)
        return Response(serializer.data)
    else:
        # option 1:
        movie = shortcuts.get_object_or_404(Movie,id=movie_id)
        serializer = AddCastSerializer(data=request.data,context={'movie_id':movie_id})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

        # option 2:
        # movie = shortcuts.get_object_or_404(Movie,id=movie_id)
        # serializer = AddCastSerializer(meta=request.data, context={'movie':movie_id})
        # serializer.is_valid(raise_exception=True)
        # serializer.save()
        # return Response(serializer.data)
    
        # option 3
        # get_object_or_404(Movie,id=movie_id)
        # data = request.data.copy()
        # data['movie'] = movie_id
        # serializer = AddCastSerializer(data = data)
        # serializer.is_valid(raise_exception=True)
        # serializer.save()
        # return Response(serializer.data)
        
# @api_view(['GET'])
# def get_movie_oscars(request:Request, movie_id:int):
    
#     movie = shortcuts.get_object_or_404(Movie,id=movie_id)
#     qs =movie.oscar_set.all()
#     serializer = OscarSeralizer(instance=qs, many=True)
#     return Response(serializer.data)
    
# @api_view(['GET'])
# def test(request:Request):
#     query_params = request.query_params
#     movies_qs = Movie.objects.all()
    
#     # for param, value in query_params.items():
#     #     pass
    
#     if 'name' in query_params:
#         movies_qs = movies_qs.filter(name__iexact=query_params['name'])
    
#     if 'duration_from' in query_params:
#         movies_qs = movies_qs.filter(duration_in_min__gte=query_params['duration_from'])
#     if 'duration_to' in query_params:
#         movies_qs = movies_qs.filter(duration_in_min__lte=query_params['duration_to'])
#     if 'description' in query_params:
#         movies_qs = movies_qs.filter(description__icontines=query_params['description'])

#     serializer = MovieSerializer(instance=movies_qs, many=True)
    
#     return Response(serializer.data)

@api_view(['GET'])
def get_version(request):
    return Response({'version':1.2})


@api_view(['GET', 'POST'])
def get_oscar(request:Request):
    
    if request.method == 'GET':
        oscars = Oscar.objects.all()
        serializer = MovieSerializer2(instance=oscars, many=True)
        return Response(serializer.data)