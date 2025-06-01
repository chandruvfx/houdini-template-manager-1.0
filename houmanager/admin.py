from django.contrib import admin

# Register your models here.
from .models import BundlesTag, Bundles
admin.site.register(BundlesTag)
admin.site.register(Bundles)
