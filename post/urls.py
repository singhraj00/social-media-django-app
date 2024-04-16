from django.urls import path 
from .views import * 

urlpatterns = [
     path('home/', index, name='index'),
    path('newpost/', new_post, name='newpost'),
    path('addstory/',add_story,name='addstory'),
    path('<uuid:post_id>', post_detail, name='post-details'),
    path('tag/<slug:tag_slug>', tags, name='tags'),
    path('<uuid:post_id>/like', like, name='like'),
    path('<uuid:post_id>/favourite', favourite, name='favourite'),

]