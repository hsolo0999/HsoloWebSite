from django.urls import path
from .views import *

urlpatterns = [
    path('', lines_show, name='nb_lines_url'),
    path('lines/create/', NbLineCreate.as_view(), name='nb_line_create_url'),
    path('line/<str:slug>/', NbLineDetail.as_view(), name='nb_line_details_url'),
    #path('line/<str:slug>/edit/', NbLineEdit.as_view(), name='nb_line_edit_url'),
    path('line/<str:slug>/delete/', NbLineDelete.as_view(), name='nb_line_delete_url'),
    path('tags/', tags_show, name='nb_tags_url'),
    path('tags/create/', NbTagCreate.as_view(), name='nb_tag_create_url'),
    path('tag/<str:slug>/', NbTagDetail.as_view(), name='nb_tag_details_url'),
    #path('tag/<str:slug>/edit/', NbTagEdit.as_view(), name='nb_tag_edit_url'),
    path('tag/<str:slug>/delete/', NbTagDelete.as_view(), name='nb_tag_delete_url')
]
