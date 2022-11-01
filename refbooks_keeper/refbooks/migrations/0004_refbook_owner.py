# Generated by Django 4.1.2 on 2022-11-01 07:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('refbooks', '0003_rename_version_element_version'),
    ]

    operations = [
        migrations.AddField(
            model_name='refbook',
            name='owner',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, related_name='refbooks', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
