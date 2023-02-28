from rest_framework import serializers
from .models import User, ItemList, Item

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
            'title',
        )

class ItemListSerializer(WritableNestedModelSerializer):
    owner = serializers.SlugRelatedField(slug_field='username', read_only=True)
    listForItems = ItemSerializer(many=True, required=False)

    class Meta:
        model = ItemList
        fields = (
            'id',
            'owner',
            'title',
            'listForItems',
        )

# class MessageSerializer(serializers.ModelSerializer):
#     from_user = serializers.SerializerMethodField()
#     to_user = serializers.SerializerMethodField()
#     conversation = serializers.SerializerMethodField()

#     class Meta:
#         model = Message
#         fields = (
#             "id",
#             "conversation",
#             "from_user",
#             "to_user",
#             "content",
#             "timestamp",
#             "read",
#         )

#     def get_conversation(self, obj):
#         return str(obj.conversation.id)

#     def get_from_user(self, obj):
#         return UserSerializer(obj.from_user).data

#     def get_to_user(self, obj):
#         return UserSerializer(obj.to_user).data