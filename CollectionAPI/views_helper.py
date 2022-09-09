from .models import ServerRequest, Collection, Movies
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.tokens import RefreshToken, SlidingToken, UntypedToken
from requests_html import HTMLSession
import environ, os, json, uuid
from datetime import datetime, timedelta
from django.core import serializers
from django.db.models import Count
from collections import Counter

def requests_count(request):
	count = ServerRequest.objects.all().first()
	if request.method == 'GET':
		return {'requests' : str(count.request_count)}
	elif request.method == 'POST':
		ServerRequest.objects.filter(pk=count.id).update(request_count=0)
		return {'message': 'request count reset successfully'}

def check_field(fields, data):
	for d in fields:
		if d not in data.keys():
			return {'message' : d+' field is missing'}
		if d != "genres" and not data[d].strip():
			return {'message' : d+' field should not be empty'}
	return {}

def register(request):
	print('Hello')
	if request.method == 'GET':
		return {'message' : 'Please make post request with username and password'}
	data = request.POST
	fields = ['username', 'password']
	
	error = check_field(fields, data)
	if error:
		return error

	if User.objects.filter(username=data['username'].strip()).exists():
		return {'message' : 'User with this username already registered.'}

	password = make_password(data['password'].strip())
	user = User.objects.create_superuser(password=password, username=data['username'].strip(), email='')

	token = str(SlidingToken.for_user(user))
	token = RefreshToken.for_user(user).access_token
	token.set_exp(lifetime=timedelta(days=30))

	return {'access_token' : str(token)}

def movies():
	session = HTMLSession()
	# env = environ.Env()
	# environ.Env.read_env()

	print(os.environ.get('USERNAME'))
	# session.auth = (env('USERNAME'), env('PASSWORD'))
	for retry in range(5):
		r = session.get('https://demo.credy.in/api/v1/maya/movies/')
		if not r.status_code == 200:
			print(r.text)
			continue
	data = json.loads(r.text)
	return data

def get_fav_genres(request):
	movies = list(Collection.objects.filter(user=request.user).values('movies'))
	movies = [x['movies'] for x in movies]
	genres = Movies.objects.filter(uuid__in=movies).values('genres')
	fav_genres = []
	for x in genres:
		genre = x['genres'].split(',')
		fav_genres.extend([i.strip() for i in genre if i.strip()])
	print(fav_genres)
	fav_genres = Counter(fav_genres)
	fav_genres = fav_genres.most_common(3)
	fav_genres = ", ".join([x[0] for x in fav_genres])

	return fav_genres



def add_movie(movie):
	m = Movies.objects.filter(pk=movie['uuid'])
	if not m:
		m = Movies(**movie)
		m.save()
	else:
		m = m[0].uuid
	return m

def collections(request, **kwargs):
	if request.method == 'GET':
		uuid = kwargs.get('collection_uuid')
		if uuid:
			col = list(Collection.objects.filter(user=request.user, collection_uuid=uuid).values('movies', 'title', 'description'))
			if not col:
				return {"message" : 'This uuid not present for collection.'}
			movies = [x['movies'] for x in col]
			movies = Movies.objects.filter(uuid__in=movies)
			movies = serializers.serialize("json", movies)
			response = {'is_success' : True, 'title': col[0]['title'], 'description': col[0]['description'], 'movies' : movies}

			return response


		collection = Collection.objects.filter(user=request.user).values('collection_uuid', 'title', 'description')
		fav_genres = get_fav_genres(request)
		response = {'is_success' : True, 'data' : {'collections' : list(collection), 'favourite_genres' : fav_genres}}
		return response
	
	if request.method == 'POST':
		print(request.user)
		data = request.POST
		fields = ['title', 'description', 'movies']
		
		error = check_field(fields, data)
		if error:
			return error
		col = Collection(user=request.user, title=data['title'].strip(), description=data['description'].strip())
		col.save()
		movies = json.loads(data['movies'].strip())
		
		for movie in movies:
			fields = ['title', 'description', 'uuid', "genres"]
			error = check_field(fields, movie)
			if error:
				return error
			m = add_movie(movie)
			col.movies.add(m)

		return {"collection_uuid" : str(col.collection_uuid)}


	if request.method == 'PUT':
		uuid = kwargs.get('collection_uuid')
		if uuid:
			if not Collection.objects.filter(user=request.user, collection_uuid=uuid).exists():
				return {"message" : 'This uuid not present for collection.'}
			data = request.data
			Collection.objects.update_or_create(pk=uuid, defaults=data)
			return {"message" : 'Updated with new values'}
		else:
			return {"message" : 'Request with uuid.'}

	if request.method == 'DELETE':
		uuid = kwargs.get('collection_uuid')
		if uuid:
			if not Collection.objects.filter(user=request.user, collection_uuid=uuid).exists():
				return {"message" : 'This uuid not present for collection.'}
			Collection.objects.filter(pk=uuid).delete()
			return {"message" : 'Collection deleted.'}
		else:
			return {"message" : 'Request with uuid.'}
