# Generated by Django 3.1.7 on 2021-04-18 15:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('user_id', models.AutoField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=20)),
                ('last_name', models.CharField(max_length=40)),
                ('email', models.EmailField(max_length=60, unique=True, verbose_name='email')),
                ('phone_number', models.CharField(max_length=13, unique=True)),
                ('password', models.CharField(blank=True, max_length=20)),
                ('role', models.CharField(default='normal-user', max_length=20, verbose_name='role')),
                ('national_code', models.CharField(blank=True, max_length=10, null=True, unique=True)),
                ('gender', models.CharField(blank=True, choices=[('Male', 'Male'), ('Female', 'Female')], max_length=10, null=True)),
                ('birthday', models.DateField(blank=True, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='users/images/')),
                ('bio', models.TextField(blank=True, null=True)),
                ('username', models.CharField(max_length=30, unique=True, verbose_name='username')),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='date joined')),
                ('last_login', models.DateTimeField(auto_now=True, verbose_name='last login')),
                ('is_admin', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='VerificationCode',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=60, unique=True, verbose_name='email')),
                ('vc_code', models.CharField(max_length=6)),
                ('time_generated', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('document_id', models.AutoField(primary_key=True, serialize=False)),
                ('file', models.FileField(upload_to='users/documents/')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='documents', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
