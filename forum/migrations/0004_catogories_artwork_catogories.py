# Generated by Django 5.1.5 on 2025-01-22 12:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0003_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Catogories',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Uncategorized', max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='artwork',
            name='catogories',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='forum.catogories'),
            preserve_default=False,
        ),
    ]
