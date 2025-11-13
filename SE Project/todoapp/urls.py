from django.urls import path
from . import views

urlpatterns = [
    path("todos/", views.todos_list),
    path("todos/<str:todo_id>/", views.todo_detail),
]
