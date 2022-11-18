# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path
from apps.home import views
from django.urls import path

from . import consumers

websocket_urlpatterns = [
  path('ws//', consumers.ChatConsumer.as_asgi()), # Using asgi
]

urlpatterns = [

    # The home page
    path('', views.index, name='home'),
    path('userprofile/<int:id>', views.userprofile, name='userprofile'),
    path('profile/', views.profileView, name="profile"),
    path('edit-profile/<int:id>', views.editprofileView, name="edit_profile"),
    path('view-user-profile/<int:id>', views.userViewProfileView, name="user_view_profile"),

    path('addpost/', views.addpost, name="addpost"),
    path('add/like/', views.addLikeByUser, name="add_like_by_user"),
    # chat
    path('chat', views.message_chat, name='message_chat'),

    path('add-friend', views.send_friend_request, name='add_friend_request'),
    path('request-accept', views.accept_friend_request, name='request_accept'),

    # ajax
    # view increase
    path('view-increase', views.view_increase, name='view_increase'),
    #comment-save
    path('comment-save', views.comment_save, name='comment_save'),
    #follow-save
    path('follow-save', views.follow_save, name='follow_save'),
    #search
    path('search', views.search, name='search'),

    # Matches any html file
    # re_path(r'^.*\.*', views.pages, name='pages'),

]
