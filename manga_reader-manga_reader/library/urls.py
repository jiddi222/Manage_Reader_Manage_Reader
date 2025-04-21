from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_login, name='login'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('book/<int:book_id>/', views.book_detail, name='book_detail'),
    path('purchase/<int:book_id>/', views.purchase_book, name='purchase_book'),
    path('logout/', views.user_logout, name='logout'),
    path('book/<int:book_id>/add_chapter/', views.add_chapter, name='add_chapter'),
    path('book/<int:book_id>/chapter/<int:chapter_id>/', views.read_chapter, name='read_chapter'),
]