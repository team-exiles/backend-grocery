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
    shared_users = UserSerializer(many=True, required=False)
    listForItems = ItemSerializer(many=True, required=False)

    class Meta:
        model = ItemList
        fields = (
            'id',
            'owner',
            'shared_users',
            'title',
            'archived',
            'created_at',
            'listForItems',
        )

    # def create(self, validated_data):
    #     return ItemList.objects.create(**validated_data)

    # def update(self, instance, validated_data):
    #     instance.name = validated_data.get('name', instance.name)
    #     instance.users = validated_data.get('users', instance.users)
    #     instance.save()
    #     return instance
    
# class InvitationSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Invitation
#         fields = (
#             'id',
#             'list',
#             'user',
#             'invited_by',
#         )

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