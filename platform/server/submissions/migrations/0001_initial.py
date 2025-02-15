# Generated by Django 4.2 on 2024-09-27 17:31

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('abstract', models.TextField()),
                ('submission_date', models.DateField(auto_now_add=True)),
                ('review_status', models.CharField(choices=[('pending', 'Pending'), ('reviewed', 'Reviewed')], default='pending', max_length=50)),
                ('categories', models.JSONField(blank=True, default=list)),
                ('authors', models.ManyToManyField(related_name='authored_papers', to=settings.AUTH_USER_MODEL)),
                ('reviewers', models.ManyToManyField(blank=True, related_name='assigned_reviews', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
