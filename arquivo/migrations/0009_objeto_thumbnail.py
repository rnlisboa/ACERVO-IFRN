# Generated by Django 4.1.4 on 2022-12-17 01:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('arquivo', '0008_categoria_slug_produtor_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='objeto',
            name='thumbnail',
            field=models.FileField(default='', upload_to='arquivos/principal/%Y/%m/%d/', verbose_name='Arquivo'),
        ),
    ]