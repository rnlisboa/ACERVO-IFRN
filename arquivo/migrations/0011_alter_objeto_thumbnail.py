# Generated by Django 4.1.4 on 2022-12-17 19:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('arquivo', '0010_alter_objeto_thumbnail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='objeto',
            name='thumbnail',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
