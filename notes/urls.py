from django.urls import path
from notes import views

urlpatterns = [
    path('', views.NoteAPIList.as_view(), name='notes_list'),
    path('edit/<int:pk>/', views.NoteAPIUpdate.as_view(), name='note_edit'),
    path('delete/<int:pk>/', views.NoteAPIDestroy.as_view(), name='note_delete'),
]