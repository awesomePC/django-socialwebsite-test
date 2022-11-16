"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib import admin
from django.urls import path,re_path, include # add this\
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView, ListView
from django.contrib.auth.decorators import login_required

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.contrib.auth.models import AbstractBaseUser
from typing import List

UserModel = get_user_model()

class UsersListView(LoginRequiredMixin, ListView):
    http_method_names = ['get', ]

    def get_queryset(self):
        return UserModel.objects.all().exclude(id=self.request.user.id)

    def render_to_response(self, context, **response_kwargs):
        users: List[AbstractBaseUser] = context['object_list']

        data = [{
            "username": user.get_username(),
            "pk": str(user.pk)
        } for user in users]
        return JsonResponse(data, safe=False, **response_kwargs)

urlpatterns = [
    # path('admin/', admin.site.urls),
    # path('', include("apps.authentication.urls")),
    #  # ADD NEW Routes HERE

    # # Leave `Home.Urls` as last the last line
    # # path("", include("apps.accounts.urls")),
    # path("", include("apps.home.urls")),

    # path('jet/', include('jet.urls')),  # Django JET URLS
    # path('jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')), # Django JET dashboard URLS

    path('admin/', admin.site.urls), # Django admin route
    path("", include("apps.authentication.urls")), # Auth routes - login / register

    # ADD NEW Routes HERE

    # Leave `Home.Urls` as last the last line
    path("", include("apps.accounts.urls")),
    path("", include("apps.home.urls")),
    #chat
    # path('', login_required(TemplateView.as_view(template_name='base.html')), name='home'),
    # path('users/', UsersListView.as_view(), name='users_list'),
    # re_path('', include("apps.chat.urls", namespace='chat')),
 
    
]
