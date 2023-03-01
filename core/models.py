from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    def __str__(self):
        return self.username

class ItemList(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ItemLists')
    title = models.CharField(max_length=50)
    archived = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True, null=True)

    def __str__(self):
        return f'{self.title}'

class Item(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Owner', null=True)
    list_for_items = models.ForeignKey(ItemList, on_delete=models.CASCADE, related_name='listForItems', null=True)
    item = models.CharField(max_length=50)
    check_box = models.BooleanField(default=False)
    # quantity = models.CharField(max_length=50, null=True)

    def __str__(self):
        return f'{self.item}'
