# Generated by Django 4.2.8 on 2024-01-31 12:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('post', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='StoryProfile',
            fields=[
                ('uid', models.UUIDField(default=uuid.uuid1, editable=False, primary_key=True, serialize=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Story',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='status')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='status', to='post.storyprofile')),
            ],
        ),
    ]