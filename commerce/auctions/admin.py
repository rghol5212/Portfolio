from django.contrib import admin
from .models import *

admin.site.register(User)
admin.site.register(Categories)
admin.site.register(ActiveListing)
admin.site.register(Watchlist)
admin.site.register(Comments)

