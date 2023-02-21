from rest_framework import serializers
from .models import User, ItemList

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
        )

class ItemListSerializer(serializers.ModelSerializer):
    owner = serializers.SlugRelatedField(slug_field='username', read_only=True)
    
    class Meta:
        model = ItemList
        fields = (
            'id',
            'owner',
            'title',
            'check_box',
            'item',
            'quantity',
        )