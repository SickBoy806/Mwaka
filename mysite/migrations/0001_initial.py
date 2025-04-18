# Generated by Django 5.0.11 on 2025-04-17 17:14

import django.contrib.auth.models
import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='DodomaDog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('microchip_id', models.CharField(blank=True, max_length=200, null=True)),
                ('behavioral_notes', models.TextField(blank=True, null=True)),
                ('breed', models.CharField(blank=True, max_length=200, null=True)),
                ('name', models.CharField(max_length=200)),
                ('origin', models.CharField(max_length=200)),
                ('date_of_birth', models.DateField()),
                ('gender', models.CharField(choices=[('male', 'Male'), ('female', 'Female')], max_length=10)),
                ('work', models.CharField(blank=True, max_length=200, null=True)),
                ('training_details', models.TextField(blank=True, null=True)),
                ('weight', models.FloatField(blank=True, null=True)),
                ('treatment_details', models.TextField(blank=True, null=True)),
                ('transfer_details', models.TextField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DodomaHorse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('microchip_id', models.CharField(blank=True, max_length=200, null=True)),
                ('behavioral_notes', models.TextField(blank=True, null=True)),
                ('breed', models.CharField(blank=True, max_length=200, null=True)),
                ('name', models.CharField(max_length=200)),
                ('origin', models.CharField(max_length=200)),
                ('date_of_birth', models.DateField()),
                ('gender', models.CharField(choices=[('male', 'Male'), ('female', 'Female')], max_length=10)),
                ('work', models.CharField(blank=True, max_length=200, null=True)),
                ('training_details', models.TextField(blank=True, null=True)),
                ('weight', models.FloatField(blank=True, null=True)),
                ('treatment_details', models.TextField(blank=True, null=True)),
                ('transfer_details', models.TextField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='HQDog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('microchip_id', models.CharField(blank=True, max_length=200, null=True)),
                ('behavioral_notes', models.TextField(blank=True, null=True)),
                ('breed', models.CharField(blank=True, max_length=200, null=True)),
                ('name', models.CharField(max_length=200)),
                ('origin', models.CharField(max_length=200)),
                ('date_of_birth', models.DateField()),
                ('gender', models.CharField(choices=[('male', 'Male'), ('female', 'Female')], max_length=10)),
                ('work', models.CharField(blank=True, max_length=200, null=True)),
                ('training_details', models.TextField(blank=True, null=True)),
                ('weight', models.FloatField(blank=True, null=True)),
                ('treatment_details', models.TextField(blank=True, null=True)),
                ('transfer_details', models.TextField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='HQHorse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('microchip_id', models.CharField(blank=True, max_length=200, null=True)),
                ('behavioral_notes', models.TextField(blank=True, null=True)),
                ('breed', models.CharField(blank=True, max_length=200, null=True)),
                ('name', models.CharField(max_length=200)),
                ('origin', models.CharField(max_length=200)),
                ('date_of_birth', models.DateField()),
                ('gender', models.CharField(choices=[('male', 'Male'), ('female', 'Female')], max_length=10)),
                ('work', models.CharField(blank=True, max_length=200, null=True)),
                ('training_details', models.TextField(blank=True, null=True)),
                ('weight', models.FloatField(blank=True, null=True)),
                ('treatment_details', models.TextField(blank=True, null=True)),
                ('transfer_details', models.TextField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='IringaDog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('microchip_id', models.CharField(blank=True, max_length=200, null=True)),
                ('behavioral_notes', models.TextField(blank=True, null=True)),
                ('breed', models.CharField(blank=True, max_length=200, null=True)),
                ('name', models.CharField(max_length=200)),
                ('origin', models.CharField(max_length=200)),
                ('date_of_birth', models.DateField()),
                ('gender', models.CharField(choices=[('male', 'Male'), ('female', 'Female')], max_length=10)),
                ('work', models.CharField(blank=True, max_length=200, null=True)),
                ('training_details', models.TextField(blank=True, null=True)),
                ('weight', models.FloatField(blank=True, null=True)),
                ('treatment_details', models.TextField(blank=True, null=True)),
                ('transfer_details', models.TextField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='IringaHorse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('microchip_id', models.CharField(blank=True, max_length=200, null=True)),
                ('behavioral_notes', models.TextField(blank=True, null=True)),
                ('breed', models.CharField(blank=True, max_length=200, null=True)),
                ('name', models.CharField(max_length=200)),
                ('origin', models.CharField(max_length=200)),
                ('date_of_birth', models.DateField()),
                ('gender', models.CharField(choices=[('male', 'Male'), ('female', 'Female')], max_length=10)),
                ('work', models.CharField(blank=True, max_length=200, null=True)),
                ('training_details', models.TextField(blank=True, null=True)),
                ('weight', models.FloatField(blank=True, null=True)),
                ('treatment_details', models.TextField(blank=True, null=True)),
                ('transfer_details', models.TextField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TpsMoshiDog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('microchip_id', models.CharField(blank=True, max_length=200, null=True)),
                ('behavioral_notes', models.TextField(blank=True, null=True)),
                ('breed', models.CharField(blank=True, max_length=200, null=True)),
                ('name', models.CharField(max_length=200)),
                ('origin', models.CharField(max_length=200)),
                ('date_of_birth', models.DateField()),
                ('gender', models.CharField(choices=[('male', 'Male'), ('female', 'Female')], max_length=10)),
                ('work', models.CharField(blank=True, max_length=200, null=True)),
                ('training_details', models.TextField(blank=True, null=True)),
                ('weight', models.FloatField(blank=True, null=True)),
                ('treatment_details', models.TextField(blank=True, null=True)),
                ('transfer_details', models.TextField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TpsMoshiHorse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('microchip_id', models.CharField(blank=True, max_length=200, null=True)),
                ('behavioral_notes', models.TextField(blank=True, null=True)),
                ('breed', models.CharField(blank=True, max_length=200, null=True)),
                ('name', models.CharField(max_length=200)),
                ('origin', models.CharField(max_length=200)),
                ('date_of_birth', models.DateField()),
                ('gender', models.CharField(choices=[('male', 'Male'), ('female', 'Female')], max_length=10)),
                ('work', models.CharField(blank=True, max_length=200, null=True)),
                ('training_details', models.TextField(blank=True, null=True)),
                ('weight', models.FloatField(blank=True, null=True)),
                ('treatment_details', models.TextField(blank=True, null=True)),
                ('transfer_details', models.TextField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('role', models.CharField(choices=[('admin', 'Admin'), ('user', 'User'), ('veterinarian', 'Veterinarian')], default='user', max_length=20)),
                ('location', models.CharField(choices=[('hq', 'Headquarters'), ('tps_moshi', 'TPS Moshi'), ('dodoma', 'Dodoma'), ('iringa', 'Iringa'), ('all', 'All Locations')], default='hq', max_length=20)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='ActivityLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.CharField(max_length=255)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('object_id', models.IntegerField()),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='MedicalRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('description', models.TextField()),
                ('doctor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='medical_records', to=settings.AUTH_USER_MODEL)),
                ('dog', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='medical_records', to='mysite.hqdog')),
                ('horse', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='medical_records', to='mysite.hqhorse')),
            ],
        ),
        migrations.CreateModel(
            name='Picture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='pictures/')),
                ('title', models.CharField(blank=True, max_length=255)),
                ('animal_type', models.CharField(choices=[('dog', 'Dog'), ('horse', 'Horse'), ('other', 'Other')], default='dog', max_length=20)),
                ('location', models.CharField(choices=[('hq', 'HQ'), ('tps_moshi', 'TPS Moshi'), ('dodoma', 'Dodoma'), ('iringa', 'Iringa')], default='hq', max_length=20)),
                ('age_description', models.CharField(blank=True, max_length=100)),
                ('related_object_id', models.IntegerField(blank=True, null=True)),
                ('related_object_name', models.CharField(blank=True, max_length=255)),
                ('force_no', models.CharField(blank=True, max_length=50, verbose_name='Force Number')),
                ('name', models.CharField(blank=True, max_length=100)),
                ('origin', models.CharField(blank=True, max_length=200)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('gender', models.CharField(blank=True, max_length=20)),
                ('work', models.TextField(blank=True)),
                ('training_details', models.TextField(blank=True)),
                ('medical_records', models.TextField(blank=True)),
                ('weight', models.CharField(blank=True, max_length=50)),
                ('vaccination_record', models.TextField(blank=True)),
                ('treatment_record', models.TextField(blank=True)),
                ('deworming_record', models.TextField(blank=True)),
                ('transfer_detail', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('uploaded_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='uploaded_pictures', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
