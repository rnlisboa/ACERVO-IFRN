# Generated by Django 4.1.4 on 2022-12-14 01:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('arquivo', '0002_objeto_created_at_alter_categoria_nome_categoria_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='objeto',
            name='publicado',
            field=models.BooleanField(default=True),
        ),
    ]
