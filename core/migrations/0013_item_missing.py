# Generated by Django 4.1.7 on 2023-03-06 01:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_alter_itemlist_auth_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='missing',
            field=models.BooleanField(default=False),
        ),
    ]
