from rest_framework import serializers
from .models import User, ItemList, Item, Invitation

from drf_writable_nested import WritableNestedModelSerializer

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
        )

class ItemSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='username', read_only=True)
    title = serializers.StringRelatedField(many=False)

    class Meta:
        model = Item
        fields = (
            'id',
            'user',
            'list_for_items',
            'item',
            'check_box',
            'missing',
            'title',
        )

class ItemListSerializer(WritableNestedModelSerializer):
    owner = serializers.SlugRelatedField(slug_field='username', read_only=True)
    shared_users = UserSerializer(many=True, required=False)
    listForItems = ItemSerializer(many=True, required=False)

    class Meta:
        model = ItemList
        fields = (
            'id',
            'auth_id',
            'owner',
            'shared_users',
            'title',
            'active_shopping',
            'archived',
            'created_at',
            'listForItems',
        )
    
class InvitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invitation
        fields = (
            'id',
            'list',
            'user',
            'invited_by',
        )