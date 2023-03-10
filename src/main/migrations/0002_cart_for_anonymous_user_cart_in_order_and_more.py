# Generated by Django 4.1.7 on 2023-02-27 12:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='for_anonymous_user',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='cart',
            name='in_order',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='notebook',
            name='image',
            field=models.ImageField(blank=True, upload_to='img/', verbose_name='Изображение'),
        ),
        migrations.AlterField(
            model_name='notebook',
            name='weight',
            field=models.CharField(blank=True, max_length=255, verbose_name='Вес'),
        ),
        migrations.AlterField(
            model_name='smartphone',
            name='image',
            field=models.ImageField(blank=True, upload_to='img/', verbose_name='Изображение'),
        ),
    ]
