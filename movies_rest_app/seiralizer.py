import datetime as dt
from rest_framework import serializers
from movies_rest_app.models import *

class ActorSerializer(serializers.ModelSerializer):
       
    class Meta:
        model = Actor
        exclude = ['birth_year']

# class DetailedActorSerializer(serializers.ModelSerializer):
       
#     class Meta:
#         model = Actor
#         fields = '__all__' 

class MovieSerializer(serializers.ModelSerializer):
    
    actors = ActorSerializer(many=True)
    
    class Meta:
        model = Movie
        # fields = '__all__'
        # fields = ['id','name','release_year']
        exclude = ['actors', 'description'] 
        # fields = '__all__'
        # depth = 1

####### get_movies ; get movie
class MovieSerializer2(serializers.ModelSerializer):
    
    class Meta:
        model = Movie
        # fields = ['id','name','description','duration_in_min','release_year'] 
        exclude = ['actors','pic_url']
        extra_kwargs = {'id':{'read_only':True},
                        'duration_in_min':{'allow_null':True},
                        'description':{'required':False},}

# get movie
class MovieDetailesSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Movie
        exclude = ['actors'] 

    
# class CreateMovieSerializer(serializers.ModelSerializer):
    
#     class Meta:
#         model = Movie
#         fields = ['id','name','description','duration_in_min','release_year']
#         kwargs = {'id':{'readonly':True}}

# def before_current_year(value):
#     if value > dt.date.today().year:
#         raise serializers.ValidationError('Before curr year')

# class CreateMovieRawSerializer(serializers.Serializer):
    
#     def create(self, validated_data):
#         movie = Movie.objects.create(**validated_data)
#         return movie
    
#     name = serializers.CharField()
#     description = serializers.CharField(required=False)
#     duration_in_min = serializers.FloatField()
#     release_year = serializers.IntegerField(
#         validators=[MaxValueValidator(2000), before_current_year])
    
#     def validate(self, attrs):
#         if attrs.get('name') == attrs.get('description'):
#             raise serializers.ValidationError('name and desc can not be equal','same_content')
#         return super().validate(attrs)

# get_movie_actors
class MovieActorsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = MovieActor
        
        exclude = ['id','movie']
        extra_kwargs = {'movie':{'write_only':True}}
                        # 'id':{'read_only':True}}
        depth = 1         

# add actor to movie - option 1
class AddCastSerializer(serializers.Serializer):
    
    actor = serializers.PrimaryKeyRelatedField(queryset=Actor.objects.all())
    salary = serializers.IntegerField()
    main_role = serializers.BooleanField()
    
    def create(self, validated_data):
        return MovieActor.create(movie_id=self.context['movie_id'],**validated_data)

# add actor to movie - option 2
# class AddCastSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = MovieActor
#         fields = ['actor','salary','main_role']
        
#     def create(self, validated_data):
#         validated_data['movie'] = self.context['movie']
#         return super().create(validated_data)

#add actor to movie - option 3
# class AddCastSerializer(serializers.ModelSerializer):
    
#     class Meta:
#         model = ['actor','salary','main_role','movie']
#         extra_kwargs = {'movie':{'write_only':True}}
#         # actor can be only once in a movie
#         validators = [
#             serializers.UniqueTogetherValidator(
#             queryset = MovieActor.objects.all(),
#             fields = ['actor','movie']
#             )
#         ]


#### get actor
class ActorSerializer1(serializers.ModelSerializer):
    
    class Meta:
        model = Actor
        fields = '__all__'
        
class ActorSerializer2(serializers.Serializer):
    
    name = serializers.CharField()
    birth_day = serializers.IntegerField()


class OscarActorSeralizer(serializers.ModelSerializer):
    
    class Meta:
        model = Actor
        fields = ['id','name']

class OscarSeralizer(serializers.ModelSerializer):
    
    class Meta:
        model = Oscar
        fields = '__all__' #['movie','actor']  
    
    def validate(self, attrs):
        msg="you can't change the following attributes: " 
        test1 = attrs.get('nominations_type')
        test2 = attrs.get('year')
        if test1:
            msg += 'nominations_type'
        
        if test2:
            if test1:
                msg += ', '
            msg += 'year'
        if len(msg) > 43:
            raise ValidationError(msg)
        return super().validate(attrs)

# def actor_oscar(value):
#     nominations_types = ['Best Actor']#,'actor':['best_actor']}
#     if value not in nominations_types:
#         raise ValidationError('This is a movie only oscar!')    
            
class NewOscarSeralizer(serializers.ModelSerializer):
    
    actor = serializers.PrimaryKeyRelatedField(queryset=Actor.objects.all())
    movie = serializers.PrimaryKeyRelatedField(queryset=Movie.objects.all())
    
    class Meta:
        model = Oscar
        fields = '__all__'
        depth = 1
        
    def validate(self, attrs):
        actors_nominations_types = ['Best Actor']#,'actor':['best_actor']}
        test1 = attrs.get('nominations_type') not in actors_nominations_types
        test2 = attrs.get('actor') != None
        if test1 and test2:
            raise ValidationError('This is a movie only oscar!')
        return super().validate(attrs)
    # def validate(self, attrs):
#         if attrs.get('name') == attrs.get('description'):
#             raise serializers.ValidationError('name and desc can not be equal','same_content')
#         return super().validate(attrs)

class MovieOscarSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Movie
        fields = ['id','name']
    pass

class ActorOscarSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Actor
        fields = ['id','name']
    pass