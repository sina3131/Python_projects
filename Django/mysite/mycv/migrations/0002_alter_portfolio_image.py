# Generated by Django 4.1.7 on 2023-03-26 18:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mycv', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='portfolio',
            name='image',
            field=models.FilePathField(path='C:\\Django\\laboration_2\\webbramverk-laboration-2-sina3131\\Version-3\\mysite\\static\\img'),
        ),
    ]
