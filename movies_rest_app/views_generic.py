from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import viewsets
from movies_rest_app.models import *
from movies_rest_app.seiralizer import *
from django_filters.rest_framework import DjangoFilterBackend,FilterSet
from django.db.models import Max,Count
import django_filters


# Create your views here.
class MovieFilterSet(FilterSet):
    
    name = django_filters.CharFilter(field_name='name', lookup_expr='iexact')
    duration_from = django_filters.NumberFilter('duration_in_min', lookup_expr='gte')
    
    class Meta:
        model = Movie
        # fields = ['name']
        fields = {
            'name':['iexact']
        }

class MovieViewSet(viewsets.ModelViewSet):
    
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer2
    # filter_backends = [DjangoFilterBackend] #becuse we set at the settings.py REST_FRAMEWORK
    filterset_class = MovieFilterSet
    
    # to overwrite the defult serializer class and assign
    # diffrent serializers to diffrent requests
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return MovieDetailesSerializer
        else:        
            return super().get_serializer_class()
        
    # def get_serializer_context(self):
        
    #     context = super().get_serializer_context()
    #     context['name']='Avner'
    #     return context
    
    
    ################ ADD ACTORS SEC
    # detail=True-> movies/movie_id/movie_actors
    # detail=False-> movies/movie_actors
    #  detail=True, url_path='actors'-> movies/movie_id/actors
    
    @action(methods=['GET'], detail=True, url_path='actors')
    def movie_actors(self, request:Request, pk):
        movie = self.get_object()
        qs =movie.movieactor_set.all()
        serializer = MovieActorsSerializer(instance=qs, many=True)
        return Response(serializer.data)
    
class OscarFilterSet(FilterSet):
    
    from_year = django_filters.NumberFilter(field_name='year', lookup_expr='gte')
    to_year = django_filters.NumberFilter(field_name='year', lookup_expr='lte')
    
    class Meta:
        model = Oscar
        # fields = ['year','nominations_type','actor','movie']
        fields = '__all__'
            
class OscarViewSet(viewsets.ModelViewSet):
    queryset = Oscar.objects.all()
    serializer_class = NewOscarSeralizer
    filterset_class = OscarFilterSet
    
    def get_serializer_class(self):
        if self.action in ['partial_update','update']:
            return OscarSeralizer
        else:        
            return super().get_serializer_class()
    
    @action(methods=['GET'], detail=False, url_path='years')
    def oscar_years(self, request:Request):
        oscar_year = int(request.query_params['year'])
        qs =Oscar.objects.filter(year__exact=oscar_year)
        serializer = NewOscarSeralizer(instance=qs, many=True)
        return Response(serializer.data)
    
    @action(methods=['GET'], detail=False)
    def movie_with_most_oscars(self, request:Request):
        
        result = Oscar.objects.annotate(count1=Count('movie'))
        movie = result.order_by('-count1')[0].movie
        print(movie)
        serializer = MovieOscarSerializer(instance=movie, many=False)
        return Response(serializer.data)    
    
    @action(methods=['GET'], detail=False)
    def actor_with_most_oscars(self, request:Request):
        
        result = Oscar.objects.annotate(count1=Count('actor'))
        actor = result.order_by('-count1')[0].actor
        print(actor)
        serializer = ActorOscarSerializer(instance=actor, many=False)
        return Response(serializer.data)    

    
    @action(methods=['GET'], detail=False)
    def total_oscars(self, request:Request):
        
        result = Oscar.objects.count()
        print(result)
        return Response(result)    
  
