from re import template
from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views


urlpatterns = [

#path('login', views.login_request, name="Login"),
path('register', views.register, name="Register"),
path('logout', views.logout_usuario, name='Logout'),
#path('editar_usuario', views.editar_usuario, name='editar_usuario'),
#path('editar_avatar', views.editar_avatar, name='editar_avatar'),
#path('borrar_avatar/<int:id>', views.borrar_avatar, name='borrar_avatar'),
#path('cambiar_password', views.cambiar_password, name='cambiar_password'),

path('password_reset/',auth_views.PasswordResetView.as_view(template_name='password_reset_form.html'),name='password_reset'),
path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'),name='password_reset_done'),
path('password-reset-confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),name='password_reset_confirm'),
path('reset/done/',auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),name='password_reset_complete'),
]