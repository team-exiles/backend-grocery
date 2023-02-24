# Generated by Django 4.1.7 on 2023-02-23 22:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_remove_itemlist_check_box_remove_itemlist_item_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='User', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='itemlist',
            name='title',
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='list_for_items',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Items', to='core.itemlist', to_field='title'),
        ),
    ]