# Generated by Django 5.0.6 on 2024-08-03 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('findapp', '0006_delete_userprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='gamemodel',
            name='room_name',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]
