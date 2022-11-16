# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path
from apps.home import views

urlpatterns = [

    # The home page
    path('', views.index, name='home'),
    path('userprofile', views.userprofile, name='userprofile'),
    path('profile/', views.profileView, name="profile"),
    path('edit-profile/<int:id>', views.editprofileView, name="edit_profile"),
    path('view-user-profile/<int:id>', views.userViewProfileView, name="user_view_profile"),

    path('addpost/', views.addpost, name="addpost"),
    path('add/like/', views.addLikeByUser, name="add_like_by_user"),
    # chat
    path('chat', views.message_chat, name='message_chat'),

    path('add-friend', views.send_friend_request, name='add_friend_request'),
    path('request-accept', views.accept_friend_request, name='request_accept'),




    # Matches any html file
    # re_path(r'^.*\.*', views.pages, name='pages'),

]
