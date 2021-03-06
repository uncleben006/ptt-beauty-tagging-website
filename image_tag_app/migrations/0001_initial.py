# Generated by Django 3.0.5 on 2020-08-15 05:53

from django.db import migrations, models
import djongo.models.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Data',
            fields=[
                ('_id', djongo.models.fields.ObjectIdField(auto_created=True, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=256)),
                ('url', models.CharField(max_length=512)),
                ('slug', models.CharField(max_length=256)),
                ('post_time', models.CharField(max_length=256)),
                ('push', models.CharField(max_length=8)),
                ('imgs', djongo.models.fields.JSONField(default=[])),
                ('author', models.CharField(max_length=256)),
                ('comments', djongo.models.fields.JSONField(default=[])),
                ('tags', djongo.models.fields.JSONField(default={})),
                ('tags_average', djongo.models.fields.JSONField(default={})),
                ('title_tags', djongo.models.fields.JSONField(default=[])),
                ('title_tags_average', djongo.models.fields.JSONField(default={})),
                ('taggers', djongo.models.fields.JSONField(default=[])),
            ],
        ),
        migrations.CreateModel(
            name='Tags',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tags_list', djongo.models.fields.JSONField(default=[])),
                ('title_tags_list', djongo.models.fields.JSONField(default=[])),
            ],
        ),
    ]
