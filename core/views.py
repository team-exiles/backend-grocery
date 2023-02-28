from django.shortcuts import render
from .models import User, ItemList, Item
from rest_framework.generics import ListCreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from .serializers import UserSerializer, ItemListSerializer, ItemSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
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

    # def list(request, list_name):
    #     return render(request, {'list_name': list_name})

class MyLists(ListCreateAPIView):
    serializer_class = ItemListSerializer

    def get_queryset(self):
        return ItemList.objects.filter(owner=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user) 

class ListDetail(RetrieveUpdateDestroyAPIView):
    serializer_class = ItemListSerializer
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.method == 'GET':
            return ItemList.objects.all()
        return ItemList.objects.filter(owner=self.request.user)
    
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

# class CustomObtainAuthTokenView(ObtainAuthToken):
#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data["user"]
#         token, created = Token.objects.get_or_create(user=user)
#         return Response({"token": token.key, "username": user.username})