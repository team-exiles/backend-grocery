from django.shortcuts import render, get_object_or_404
from .models import User, ItemList, Item, Invitation
from rest_framework.generics import ListCreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView, UpdateAPIView
from rest_framework.views import APIView
from .serializers import UserSerializer, ItemListSerializer, ItemSerializer, InvitationSerializer
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework import status
# Create your views here.

class IsOwner(BasePermission):
    # h.o.p. perform the check and returns boolean value indicating if user has permission to perform action
    def has_object_permission(self, request, view, obj):
        # Compares by checking whether the user is the owner of the list
        return obj.owner == request.user

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
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ItemList.objects.filter(owner=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user) 

class ListDetail(RetrieveUpdateDestroyAPIView):
    serializer_class = ItemListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.method == 'GET':
            return ItemList.objects.all()
        return ItemList.objects.filter(owner=self.request.user)
    
    def perform_update(self, serializer):
        serializer.save()

    # def put(self, request, *args, **kwargs):
    #     list = self.get_object()
    #     user_id = request.data.get('user_id', None)
    #     if user_id:
    #         user = User.objects.get(id=user_id).user
    #         list.users.add(user)
    #         list.save()
    #         return Response({'status': 'user added to list'}, status=status.HTTP_200_OK)
    #     else:
    #         return Response({'status': 'user_id required'}, status=status.HTTP_400_BAD_REQUEST)


    # def put(self, request, *args, **kwargs):
    #     list_obj = self.get_object()
    #     user_id = request.data.get('user_id')
    #     action = request.data.get('action')

    #     if user_id and action:
    #         user_obj = User.objects.get(id=user_id)
    #         if action == 'add':
    #             list_obj.users.add(user_obj)
    #         elif action == 'remove':
    #             list_obj.users.remove(user_obj)
    #     return self.update(request, *args, **kwargs)
    
class ListItems(ListCreateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

    def get_queryset(self):
        return Item.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    # def perform_create(self, serializer):
    #     list_id = self.kwargs['list_id']
    #     list_obj = ItemList.objects.get(id=list_id)
    #     if list_obj.owner != self.request.user and self.request.user not in list_obj.invited_users.all():
    #         raise permissions.PermissionDenied
    #     serializer.save(list=list_obj)

class ItemDetail(RetrieveUpdateDestroyAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

class ListInviteView(UpdateAPIView):
    queryset = ItemList.objects.all()
    serializer_class = ItemListSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def put(self, request, *args, **kwargs):
        list_object = self.get_object()
        user_id = request.data.get('user_id')
        print('USER ID:', user_id)
        user = get_object_or_404(User, id=user_id)
        print('USER:', user)

        list_object.shared_users.add(user)
        list_object.save()
        serializer = self.get_serializer(list_object)
        return Response(serializer.data, status=status.HTTP_200_OK)


# class InviteUserView(APIView):
#     serializer_class = InvitationSerializer

#     def post(self, request):
#         user_id = request.data.get('user_id')
#         itemlist_id = request.data.get('itemlist_id')
#         invited_by = request.user

#         try:
#             user = User.objects.get(id=user_id)
#         except User.DoesNotExist:
#             return Response({'error': 'User not found'}, status=status.HTTP_201_CREATED)

#         try:
#             itemlist = ItemList.objects.get(id=itemlist_id, owner=request.user)
#         except ItemList.DoesNotExist:
#             return Response({'error': 'List not found'}, status=status.HTTP_404_NOT_FOUND)

#         invitation = Invitation(itemlist=itemlist, user=user, invited_by=invited_by)
#         invitation.save()

#         serializer = InvitationSerializer(invitation)
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
    
# class AcceptInvitationView(APIView):
#     serializer_class = InvitationSerializer

#     def get_queryset(self):
#         return Invitation.objects.filter(id=self.kwargs['invitation_id'])
    
#     def partial_update(self, request, *args, **kwargs):
#         invitation = self.get_object()
#         if 'username' in request.data:
#             user = User.objects.get(username=request.data['username'])
#             ItemList.shared_users.add(user)
#             serializer = self.get_serializer(Invitation, data=request.data, partial=True)
#             serializer.is_valid(raise_exception=True)
#             self.perform_update(serializer)
#             return JsonResponse({'message': f'{user} has left the group'}, status=200)


#     def post(self, request):
#         invitation_id = request.data.get('invitation_id')
#         item_list = ItemList.objects.get(id=request.data['itemlist_id'])
#         user = User.objects.get(id=request.data['user_id'])
#         try:
#             invitation = Invitation.objects.get(id=invitation_id, user=request.user)
#         except Invitation.DoesNotExist:
#             return
#         item_list.shared_users.add(user)
#         invitation.save()

# class RejectInvitationView(APIView):
#     def post(self, request):
#         invitation_id = request.data.get('invitation_id')
#         item_list = ItemList.objects.get(id=request.data['itemlist_id'])
#         user = User.objects.get(id=request.data['user_id'])
#         try:
#             invitation = Invitation.objects.get(id=invitation_id, user=request.user)
#         except Invitation.DoesNotExist:
#             return
#         item_list.shared_users.add(user)
#         invitation.save()

# class CustomObtainAuthTokenView(ObtainAuthToken):
#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data["user"]
#         token, created = Token.objects.get_or_create(user=user)
#         return Response({"token": token.key, "username": user.username})