# Generated by Django 5.0.6 on 2024-08-11 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('findapp', '0017_friendsmodel_user2_alter_friendsmodel_user1'),
    ]

    operations = [
        migrations.AlterField(
            model_name='friendsmodel',
            name='score',
            field=models.FloatField(default=0),
        ),
    ]
