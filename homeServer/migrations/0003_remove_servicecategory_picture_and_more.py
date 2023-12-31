# Generated by Django 4.2.5 on 2023-09-16 18:21

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homeServer', '0002_alter_user_phone_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='servicecategory',
            name='picture',
        ),
        migrations.AlterField(
            model_name='servicecategory',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='bland/category/', validators=[django.core.validators.FileExtensionValidator(['png', 'jpg', 'jpeg'])], verbose_name='bland images'),
        ),
    ]
