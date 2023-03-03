from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    def __str__(self):
        return self.username

class ItemList(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ItemLists')
    shared_users = models.ManyToManyField(User, related_name='shared_lists')

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

    def __str__(self):
        return f'{self.item}'
    
# class Invitation(models.Model):
#     list = models.ForeignKey(ItemList, on_delete=models.CASCADE)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     invited_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='invitations_sent')

#     def __str__(self):
#         return f"Invitation from {self.invited_by.username} to {self.user.username} for {self.list.title}"



# class SharedWith(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ListOwner')
#     shared_list = models.ForeignKey(User, on_delete=models.CASCADE, related_name='SharedList')
#     created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True, db_index=True)

#     class Meta:
#         constraints = [
#             models.UniqueConstraint(
#                 fields=['user', 'shared_list'], name='unique_shared'
#             )
#         ]

#     def __str__(self):
#         return f'{self.user} is now following list {self.shared_list}'