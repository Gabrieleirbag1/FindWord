# Generated by Django 5.0.6 on 2024-08-11 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('findapp', '0018_alter_friendsmodel_score'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gamemodel',
            name='player1_note',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='gamemodel',
            name='player2_note',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
    ]
