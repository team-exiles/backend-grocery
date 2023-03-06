from django.shortcuts import render, get_object_or_404
from .models import User, ItemList, Item
from rest_framework.generics import ListCreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView, UpdateAPIView
from rest_framework.views import APIView
from .serializers import UserSerializer, ItemListSerializer, ItemSerializer
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.response import Response
from rest_framework import status
# Create your views here.

class IsOwner(BasePermission):
    # h.o.p. perform the check and returns boolean value indicating if user has permission to perform action
    def has_object_permission(self, request, view, obj):
        # Compares by checking whether the user is the owner of the list
        return obj.owner == request.user
    
class IsOwnerOrSharedUser(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.owner or request.user in obj.shared_users.all()

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
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ItemList.objects.filter(owner=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user) 

class ListDetail(RetrieveUpdateDestroyAPIView):
    serializer_class = ItemListSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrSharedUser]

    def get_queryset(self):
        if self.request.method == 'GET':
            return ItemList.objects.all()
        return ItemList.objects.filter(owner=self.request.user)
    
    def perform_update(self, serializer):
        serializer.save()
    
class ListItems(ListCreateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

    def get_queryset(self):
        return Item.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ItemDetail(RetrieveUpdateDestroyAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

class ListInviteView(UpdateAPIView):
    queryset = ItemList.objects.all()
    serializer_class = ItemListSerializer

    def put(self, request, *args, **kwargs):
        list_object = self.get_object()
        username = request.data.get('username')
        user = get_object_or_404(User, username=username)

        if user == list_object.owner or user in list_object.shared_users.all():
            return Response({'detail': 'User is already a collaborator on this list.'})

        list_object.shared_users.add(user)
        list_object.save()
        serializer = self.get_serializer(list_object)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, pk=self.kwargs['pk'])
        return obj

class ListRemoveUserView(APIView):
    permission_classes = [IsAuthenticated, IsOwner]

    def delete(self, request, pk, username, format=None):
        try:
            list_object = ItemList.objects.get(pk=pk)
        except ItemList.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        user = User.objects.get(username=username)
        if user in list_object.shared_users.all():
            list_object.shared_users.remove(user)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
class SharedListAPIView(ListAPIView):
    serializer_class = ItemListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return ItemList.objects.filter(shared_users=user)