# Generated by Django 4.2.3 on 2023-07-29 20:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pereval', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pereval',
            name='status',
            field=models.CharField(choices=[('new', 'новый'), ('pending', 'модератор взял в работу'), ('accepted', 'модерация прошла успешно'), ('rejected', 'модерация прошла, информация не принята')], max_length=10),
        ),
    ]