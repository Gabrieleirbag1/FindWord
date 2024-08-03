# urls.py
from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [

    path('lobby/', views.LobbyView.as_view(), name='lobby'),
    path('', views.LobbyView.as_view(), name='lobby'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.logout_user, name='logout'),

    path("room/<str:room_name>/", login_required(views.GameView.as_view(), login_url='lobby'), name="room"),
]