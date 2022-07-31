# Generated by Django 4.0.6 on 2022-07-31 14:32

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user_id', models.PositiveBigIntegerField(primary_key=True, serialize=False)),
                ('username', models.CharField(blank=True, max_length=32, null=True)),
                ('first_name', models.CharField(max_length=256)),
                ('last_name', models.CharField(blank=True, max_length=256, null=True)),
                ('language_code', models.CharField(blank=True, max_length=8, null=True)),
            ],
            options={
                'ordering': ('-created_at',),
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('phone_number', models.CharField(max_length=256)),
                ('first_name', models.CharField(max_length=256)),
                ('last_name', models.CharField(blank=True, max_length=256, null=True)),
                ('telegram_id', models.PositiveBigIntegerField(blank=True, null=True)),
                ('group', models.CharField(choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')], max_length=1)),
                ('last_contact_date', models.DateField(default=datetime.date.today)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contacts', to='tgbot.user')),
            ],
            options={
                'ordering': ('-created_at',),
                'abstract': False,
            },
        ),
    ]
