# Generated by Django 4.1.4 on 2022-12-17 02:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('arquivo', '0009_objeto_thumbnail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='objeto',
            name='thumbnail',
            field=models.FileField(blank=True, default='', upload_to='arquivos/principal/%Y/%m/%d/', verbose_name='Thumbnail'),
        ),
    ]
