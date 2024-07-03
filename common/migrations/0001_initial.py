# Generated by Django 5.0.6 on 2024-07-02 15:28

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Media',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='only_medias/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'svg', 'webp', 'mp4', 'mpeg4', 'avi', 'mov', 'mkv', 'pdf', 'doc', 'docx', 'gif'])], verbose_name='File')),
                ('file_type', models.CharField(choices=[('image', 'Image'), ('video', 'Video'), ('document', 'Document'), ('gif', 'Gif'), ('other', 'Other')], max_length=10, verbose_name='File Type')),
            ],
            options={
                'verbose_name': 'Media',
                'verbose_name_plural': 'Media',
            },
        ),
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('main_phone_number', models.CharField(max_length=20, verbose_name='Main Phone Number')),
                ('title', models.TextField(verbose_name='Title')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('email', models.TextField(blank=True, null=True, verbose_name='e-mail')),
                ('settings_page_image', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='settings_page_image', to='common.media', verbose_name='Settings Page Image')),
            ],
            options={
                'verbose_name': 'Settings',
                'verbose_name_plural': 'Settings',
            },
        ),
    ]
