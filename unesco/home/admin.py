from django.contrib import admin

# Register your models here.

from home.models import Site, Category, Iso, Region, States

admin.site.register(Site)
admin.site.register(Category)
admin.site.register(Iso)
admin.site.register(Region)
admin.site.register(States)