# Generated by Django 5.0.6 on 2024-08-05 09:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('findapp', '0011_remove_gamemodel_player1_ready_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gamemodel',
            name='in_game_state',
            field=models.BooleanField(default=False),
        ),
    ]
