# Generated by Django 4.1.5 on 2023-02-04 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0004_alter_qrcode_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='qrcode',
            name='id_in_electron',
            field=models.IntegerField(null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='qrcode',
            name='qr',
            field=models.CharField(db_index=True, max_length=255, verbose_name='QrCode данные'),
        ),
    ]
