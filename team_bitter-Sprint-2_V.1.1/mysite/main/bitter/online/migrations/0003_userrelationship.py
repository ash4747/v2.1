# Generated by Django 2.2.5 on 2020-02-25 00:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('online', '0002_auto_20200219_2016'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserRelationship',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('selfname', models.CharField(max_length=50, unique=True)),
                ('friendname', models.CharField(max_length=50, unique=True)),
            ],
        ),
    ]
