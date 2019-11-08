# Generated by Django 2.2.6 on 2019-11-07 10:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0006_datatypes_relatedcommunity'),
    ]

    operations = [
        migrations.AddField(
            model_name='datatypes',
            name='datatypeCreationDate',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='datatypes',
            name='datatypeCreator',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='datatypecreator', to='community.communityUsers'),
        ),
        migrations.AddField(
            model_name='datatypes',
            name='datatypePhoto',
            field=models.CharField(help_text='datatype photo', max_length=200, null=True),
        ),
    ]
