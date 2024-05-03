# Generated by Django 4.0.1 on 2024-05-03 20:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tutdb', '0004_question_uuid'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='session',
            field=models.CharField(choices=[('2021/2022', '2021/2022'), ('2022/2023', '2022/2023')], default='2022/2023', max_length=100),
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField(max_length=100)),
                ('year', models.CharField(choices=[('Year 1', 'Year 1'), ('Year 2', 'Year 2'), ('Year 3', 'Year 3'), ('Year 4', 'Year 4'), ('Year 5', 'Year 5')], max_length=100)),
                ('code', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]