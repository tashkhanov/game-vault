from django.urls import path
from .views import *

urlpatterns = [
    path('', main_page, name='main'),
    path('games/', games_page, name='games'),
    path('news/', news_page, name='news'),
    path('mods/', mods_page, name='mods'),
    path('game/<int:pk>/', game_detail, name='game'),
    path('new/<int:pk>/', new_detail, name='new'),
    path('genre/<int:pk>', game_by_genre, name='genre'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),
    path('<str:target_type>/<int:target_id>/comment/add/', add_comment, name='add_comment'),
    path('comment/<int:comment_id>/edit/', edit_comment, name='edit_comment'),
    path('comment/<int:comment_id>/delete/', delete_comment, name='delete_comment'),
]
