# Generated by Django 2.2.6 on 2019-12-09 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0024_auto_20191207_1926'),
    ]

    operations = [
        migrations.AddField(
            model_name='posts',
            name='postTag',
            field=models.CharField(help_text='Enter Post Tags', max_length=200, null=True),
        ),
    ]
