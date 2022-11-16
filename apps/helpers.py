
# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import base64
import os
import random
import string

from django.conf                import settings
from storages.backends.ftp      import FTPStorage
from apps.authentication.models import User
import requests
# for map get address
API_Access_Token_Loction ='pk.1483e9bce7f8c7ec3e287bd34a9744bc'
FILE_EXTENTION =  {'.jpg', '.jpeg', '.png'}

def upload(username, image):
    file_obj = image

    # do your validation here e.g. file size/type check

    # organize a path for the file in bucket
    file_directory_within_bucket = f'{username}'

    # synthesize a full file path; note that we included the filename
    file_path_within_bucket = os.path.join(
        file_directory_within_bucket,
        file_obj.name
    )

    media_storage = FTPStorage()

    if not media_storage.exists(file_path_within_bucket):  # avoid overwriting existing file
        media_storage.save(file_path_within_bucket, file_obj)

    return media_storage.url(file_path_within_bucket)

def username_exists(username):

    user_query = User.objects.filter(username=username)
    if user_query.exists():
        return user_query.first()

    return False

def email_exists(email):

    user_query = User.objects.filter(email=email)

    if user_query.exists():
        return user_query.first()

    return False

def cfg_val( aVarName ):

    return getattr(settings, aVarName, None)

def cfg_LOGIN_ATTEMPTS():

    return cfg_val( "LOGIN_ATTEMPTS" )

def cfg_FTP_UPLOAD(): 
    return cfg_val( "FTP_UPLOAD" )

# TODO: add helper for delete User

def delete_user(to_delete_user_username):
    user = User.objects.filter(username=to_delete_user_username)
    if user.count() == 0:
        return False, 'User not found.'
    if user.last().is_superuser:
        return False, 'Cannot delete superuser.'
    try:
        user.delete()
    except Exception as e:
        return False, str(e)
    return True, f'{to_delete_user_username} deleted successfully.'


def get_current_location(lat,lng):
    """ For get current location """
    url = f"https://us1.locationiq.com/v1/reverse?key={API_Access_Token_Loction}&lat={lat}&lon={lng}&format=json"
    response = requests.get(url)
    try:
        res = response.json()
        address = res['display_name']
        lat     = res['lat']
        lng     = res['lon']

    except Exception as e:
        print(f"Error : {e}")
        return False
    return address, lat, lng

def check_extention(file_path):

    if os.path.splitext(file_path.name):
        file_extension = os.path.splitext(file_path.name)[1]
        if file_extension.lower() in FILE_EXTENTION:
            print("It's an image file")

            return file_extension.lower()
        else:
            return True