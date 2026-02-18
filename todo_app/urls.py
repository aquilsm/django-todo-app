from django.urls import path
from . import views

urlpatterns = [
    path('', views.todo_list, name='todo_list'),
    path('add/', views.add_todo, name='add_todo'),
    path('toggle/<int:todo_id>/', views.toggle_todo, name='toggle_todo'),
    path('delete/<int:todo_id>/', views.delete_todo, name='delete_todo'),
    path('edit/<int:todo_id>/', views.edit_todo, name='edit_todo'),
    path('subtask/toggle/<int:subtask_id>/', views.toggle_subtask, name='toggle_subtask'),
    path('subtask/delete/<int:subtask_id>/', views.delete_subtask, name='delete_subtask'),
    path('categories/', views.manage_categories, name='manage_categories'),
    path('categories/delete/<int:category_id>/', views.delete_category, name='delete_category'),
]
