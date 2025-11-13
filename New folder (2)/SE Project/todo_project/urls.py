from django.contrib import admin
from django.urls import path, include
from todoapp import views as todo_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("todoapp.urls")),            # API endpoints
    path("auth/", include("todoapp.urls_auth")),      # login/signup/logout
    path("", todo_views.dashboard, name="home"),      # root -> dashboard (protected)
]
