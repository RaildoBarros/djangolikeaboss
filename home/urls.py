from django.urls import path
from .views import home, my_logout, MyView

urlpatterns = [
    path('', home, name="home"),
    path('logout/', my_logout, name="logout"),
    path('view/', MyView.as_view(), name="view"),
]