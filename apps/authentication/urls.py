from django.urls import path, include
# from views
from . import views
from django.contrib.auth import views as auth_views

# from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('register/', views.register_user, name="register"),
    path('login/', views.login_view, name="login"),
    path('logout/',   views.logoutView, name='logout'),
    
    # path("change_password/", views.change_password , name='change_password'),
    
    path('password-reset/',auth_views.PasswordResetView.as_view(template_name='password_reset.html'),name='password_reset'),
    path('password-reset/done/',auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'),name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),name='password_reset_confirm'),

    path('password-reset-complete/',auth_views.PasswordResetCompleteView.as_view(
             template_name='password_reset_complete.html'),
         name='password_reset_complete'),
]
