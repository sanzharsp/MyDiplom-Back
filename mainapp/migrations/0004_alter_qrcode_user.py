# Generated by Django 4.1.5 on 2023-02-04 12:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0003_alter_profile_qrcode_alter_profile_room_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='qrcode',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
    ]
