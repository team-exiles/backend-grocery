from rest_framework import serializers
from .models import User, ItemList, Item

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
            'title',
        )

class ItemListSerializer(serializers.ModelSerializer):
    owner = serializers.SlugRelatedField(slug_field='username', read_only=True)
    listForItems = ItemSerializer(many=True)

    class Meta:
        model = ItemList
        fields = (
            'id',
            'owner',
            'title',
            'listForItems',
        )