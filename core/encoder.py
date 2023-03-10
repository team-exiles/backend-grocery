import json
from django.core.serializers.json import DjangoJSONEncoder
from .models import Item

class ItemEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, Item):
            return {
                'id': obj.id,
                'item': obj.item,
                'check_box': obj.check_box,
                'missing': obj.missing,
            }
        return super().default(obj)
