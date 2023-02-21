from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    def __str__(self):
        return self.username

class ItemList(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ItemLists')
    title = models.CharField(max_length=50)
    check_box = models.BooleanField(default=False)
    item = models.CharField(max_length=50)
    quantity = models.CharField(max_length=50, null=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    # archived = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.title}'