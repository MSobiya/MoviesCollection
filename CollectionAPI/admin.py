from django.contrib import admin

from .models import Movies, Collection

admin.site.register([Movies, Collection])

