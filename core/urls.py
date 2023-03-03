from django.urls import path
from . import views

urlpatterns = [
    path('users/', views.UserView.as_view(), name='profile'),
    path('lists/', views.ItemListsList.as_view(), name='lists'),
    path('lists/me/', views.MyLists.as_view(), name='my_lists'),
    path('lists/<int:pk>/', views.ListDetail.as_view(), name='list_detail'),
    path('items/', views.ListItems.as_view(), name='items_list'),
    path('items/<int:pk>/', views.ItemDetail.as_view(), name='item_detail'),
    # path('invite/', views.InviteUserView.as_view()),
    # path('accept-invitation/', views.AcceptInvitationView.as_view()),
]


