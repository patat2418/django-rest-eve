from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.core.exceptions import ValidationError

import datetime as dt

# Create your models here.
def before_current_year(value):
    if value > dt.date.today().year:
        raise ValidationError('Before curr year')
    
class Actor(models.Model):

    name = models.CharField(max_length=256, db_column='name', null=False, blank=False)
    birth_year = models.IntegerField(db_column='birth_year', null=False)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'actors'


class Movie(models.Model):

    name = models.CharField(max_length=256, db_column='name', null=False)
    description = models.TextField(db_column='description', null=False)
    duration_in_min = models.FloatField(db_column='duration', null=False)
    release_year = models.IntegerField(db_column='year', null=False)
    pic_url = models.URLField(max_length=512, db_column='pic_url', null=True)

    actors = models.ManyToManyField(Actor, through='MovieActor')

    # def __str__(self):
    #     return self.name

    class Meta:
        db_table = 'movies'


class Rating(models.Model):

    movie = models.ForeignKey(
        'Movie',
        on_delete=models.CASCADE,
    )
    rating = models.SmallIntegerField(db_column='rating', null=False,
                                       validators=[MinValueValidator(1), MaxValueValidator(10)])
    rating_date = models.DateField(db_column='rating_date', null=False, auto_now_add=True)


    class Meta:
        db_table = 'ratings'


class MovieActor(models.Model):
    actor = models.ForeignKey(Actor, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    salary = models.IntegerField()
    main_role = models.BooleanField(null=False, blank=False)

    def __str__(self):
        return f"{self.actor.name} in movie {self.movie.name}"


    class Meta:
        db_table = 'movie_actors'

def actor_oscar(value):
    nominations_types = ['Best Actor']#,'actor':['best_actor']}
    if value not in nominations_types:
        raise ValidationError('This is a movie only oscar!')    
        
class Oscar(models.Model):
        
    class Meta:
        db_table = 'oscar'
        unique_together = ('year','nominations_type')
    
    year = models.IntegerField(db_column='year', null=False, blank=False,
                                       validators=[before_current_year])
    nominations_type = models.CharField(max_length=256, db_column='nominations type', null=False,blank=False)
    actor = models.ForeignKey(Actor, null=True, blank=False, on_delete=models.CASCADE, )
                            #   validators=[actor_oscar])
    movie = models.ForeignKey(Movie, null=False, blank=False, on_delete=models.CASCADE)
    
    