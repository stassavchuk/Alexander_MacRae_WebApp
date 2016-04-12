from django.contrib import admin

# Register your models here.

from .models import Filing, Document

# admin.site.register(Filing)
admin.site.register(Document)
