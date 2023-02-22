from django.urls import path
from . import views

urlpatterns = [
    path('users/', views.UserView.as_view(), name='profile'),
    path('lists/', views.ItemListsList.as_view(), name='lists'),
    path('lists/me/', views.MyLists.as_view(), name='my_lists'),
    path('lists/<int:list_id>/', views.ListDetail.as_view(), name='list_detail'),
]