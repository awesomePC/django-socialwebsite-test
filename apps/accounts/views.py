# from django.shortcuts import render

# # Create your views here.

import os

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render

from apps import helpers
from apps.accounts.forms import EditProfileForm
from apps.authentication.models import User
from apps import COMMON


@login_required(login_url="/login/")
def user_list(request, **kwargs):
    # get all users
    if not request.user.is_superuser:
        return render(request, 'home/page-403.html')

    if request.method == 'GET':
        users = User.objects.all()
        form = EditProfileForm()
        return render(request, 'accounts/users-reports.html', context={
            'users': [
                {
                    **user.to_dict(),
                    'status': 0 if user.status == COMMON.USER_SUSPENDED else 1,
                }
                for user in users
            ],
            'form': form
        })

    # Update Profile
    if request.method == 'POST':
        return profile(request, edit_type='user_list', **kwargs)

    if request.method == 'PUT':
        user = User.objects.get(username=kwargs.get('username'))

        if user.status == COMMON.USER_ACTIVE:
            user.status = COMMON.USER_SUSPENDED
        else:
            user.status = COMMON.USER_ACTIVE

        user.failed_logins = 0
        user.save()
        return JsonResponse({})

    if request.method == 'DELETE':
        result, message = helpers.delete_user(kwargs.get('username'))
        return JsonResponse({
            **({
                   'message': message
               } if result else {
                'errors': message
            }),
        }, status=200 if result else 400)


@login_required(login_url="/login/")
def profile(request, **kwargs):
    if request.method == 'GET':
        user = User.objects.get(username=request.user.username)

        return render(request, 'accounts/account-settings.html', context={
            'user': user.to_dict(),
        })

    if request.method == 'POST':
        form = EditProfileForm(request.POST,
                               instance=User.objects.get(username=kwargs.get('username', request.user.username)))
        if form.is_valid():
            user = form.save()
            image = request.FILES.get('avatar-input', None)

            if helpers.cfg_FTP_UPLOAD() and image:
                try:
                    avatar_url = helpers.upload(user.username, image)
                    user.image = os.getenv("upload_url") + '/'.join(avatar_url.split("/")[-2:])
                    user.save()
                except Exception as e:
                    print(str(e))
                    print("There is a problem in connection with FTP")
                    return JsonResponse({
                        'errors': 'There is a problem in connection with FTP'
                    }, status=400)

            if kwargs.get('edit_type') == 'user_list':
                return JsonResponse({})
            else:
                return render(request, 'accounts/account-settings.html', context={
                    'user': user.to_dict()
                })

        return JsonResponse({
            'errors': form.errors
        }, status=400)
