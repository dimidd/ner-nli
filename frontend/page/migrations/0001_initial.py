# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-13 20:56
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('entities', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=500)),
                ('path', models.CharField(max_length=500, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Hit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=500)),
                ('first_word_id', models.CharField(max_length=500)),
                ('word_count', models.IntegerField()),
                ('lookup_used', models.CharField(max_length=500)),
                ('alto_info', models.TextField()),
                ('entity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hits', to='entities.Entity')),
            ],
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ordinal', models.IntegerField()),
                ('path', models.CharField(max_length=500)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pages', to='page.Book')),
            ],
        ),
        migrations.AddField(
            model_name='hit',
            name='page',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hits', to='page.Page'),
        ),
        migrations.AlterUniqueTogether(
            name='page',
            unique_together=set([('book', 'path'), ('book', 'ordinal')]),
        ),
    ]
