# Generated by Django 4.2.3 on 2023-07-30 18:52

from django.db import migrations, models
import pereval.utils


class Migration(migrations.Migration):

    dependencies = [
        ('pereval', '0003_alter_pereval_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='images',
            name='data',
            field=models.ImageField(blank=True, default='https://example.jpg', null=True, upload_to=pereval.utils.get_path_upload_photos, verbose_name='Изображение'),
        ),
    ]