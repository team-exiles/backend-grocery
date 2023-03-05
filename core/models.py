from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.serializers import serialize
import json, string, random
# Create your models here.

def random_string_generator(size=10, chars=string.digits):
    while True:
        string = ''.join(random.choice(chars) for _ in range(10))
        if ItemList.objects.filter(auth_id=string).count() == 0:
            break
    return string

class User(AbstractUser):
    def __str__(self):
        return self.username

class ItemList(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ItemLists')
    shared_users = models.ManyToManyField(User, related_name='shared_lists')

    title = models.CharField(max_length=50)
    auth_id = models.CharField(max_length=15, default=random_string_generator)
    active_shopping = models.BooleanField(default=False)
    archived = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True, null=True)

    def to_json(self):
        json_data = serialize('json', [self])
        struct = json.loads(json_data)
        data = struct[0]['fields']
        data['id'] = struct[0]['pk']
        return data

    def __str__(self):
        return f'{self.title}'

class Item(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Owner', null=True)
    list_for_items = models.ForeignKey(ItemList, on_delete=models.CASCADE, related_name='listForItems', null=True)
    item = models.CharField(max_length=50)
    check_box = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.item}'
    
class Invitation(models.Model):
    list = models.ForeignKey(ItemList, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    invited_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='invitations_sent')

    def __str__(self):
        return f"Invitation from {self.invited_by.username} to {self.user.username} for {self.list.title}"