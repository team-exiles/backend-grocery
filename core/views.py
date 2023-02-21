from django.shortcuts import render
from .models import User, ItemList
from rest_framework.generics import ListCreateAPIView, ListAPIView
from .serializers import UserSerializer, ItemListSerializer
# Create your views here.

class UserView(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        queryset = User.objects.filter(username=self.request.user)
        return queryset
    
class ItemListsList(ListAPIView):
    queryset = ItemList.objects.all()
    serializer_class = ItemListSerializer

class MyLists(ListCreateAPIView):
    serializer_class = ItemListSerializer

    def get_queryset(self):
        return ItemList.objects.filter(owner=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user) 

