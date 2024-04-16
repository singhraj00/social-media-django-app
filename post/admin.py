from django.contrib import admin
from .models import *



# Register your models here.


admin.site.register(Tag)
admin.site.register(Post)
admin.site.register(Follow)
admin.site.register(Stream)

admin.site.register(Story)

admin.site.register(StoryProfile)


