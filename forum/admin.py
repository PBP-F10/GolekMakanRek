from django.contrib import admin
from .models import Like, Comment, Report

# Register your models here.
admin.site.register(Like)
admin.site.register(Comment)
admin.site.register(Report)