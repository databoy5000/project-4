from django.contrib import admin
from .models import Crisis, Request, Resource, NGOResource

admin.site.register(Crisis)
admin.site.register(Request)
admin.site.register(Resource)
admin.site.register(NGOResource)