# Generated by Django 4.1.7 on 2023-03-29 11:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mycv', '0004_contanct'),
    ]

    operations = [
        migrations.AddField(
            model_name='contanct',
            name='country',
            field=models.TextField(default='Sweden', max_length=100),
        ),
        migrations.AddField(
            model_name='contanct',
            name='email',
            field=models.EmailField(default='example@gmail.com', max_length=254),
        ),
        migrations.AddField(
            model_name='contanct',
            name='last_name',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='contanct',
            name='message',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='contanct',
            name='mobile',
            field=models.IntegerField(default='046709135467'),
        ),
        migrations.AddField(
            model_name='contanct',
            name='name',
            field=models.CharField(default='name', max_length=100),
        ),
        migrations.AddField(
            model_name='contanct',
            name='subject',
            field=models.CharField(default='', max_length=100),
        ),
    ]
