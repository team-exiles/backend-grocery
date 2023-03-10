from django.urls import path, include
from . import views
from . import routing

urlpatterns = [
    path('users/', views.UserView.as_view(), name='profile'),
    path('lists/', views.ItemListsList.as_view(), name='lists'),
    path('lists/me/', views.MyLists.as_view(), name='my_lists'),
    path('lists/<int:pk>/', views.ListDetail.as_view(), name='list_detail'),
    path('items/', views.ListItems.as_view(), name='items_list'),
    path('items/<int:pk>/', views.ItemDetail.as_view(), name='item_detail'),
    path('lists/<int:pk>/invite/', views.ListInviteView.as_view(), name='list_invite'),
    path('lists/<int:pk>/remove/<str:username>/', views.ListRemoveUserView.as_view()),
    path('lists/shared/', views.SharedListAPIView.as_view(), name='shared_lists'),
]


