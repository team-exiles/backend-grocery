from django.contrib import admin
from .models import User, ItemList, Item, Invitation
# Register your models here.


admin.site.register(User)
admin.site.register(ItemList)
admin.site.register(Item)
admin.site.register(Invitation)