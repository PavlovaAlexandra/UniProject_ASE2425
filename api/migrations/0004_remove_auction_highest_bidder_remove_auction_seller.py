# Generated by Django 5.1.3 on 2024-11-09 16:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_player_auction_highest_bidder_auction_seller'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='auction',
            name='highest_bidder',
        ),
        migrations.RemoveField(
            model_name='auction',
            name='seller',
        ),
    ]
