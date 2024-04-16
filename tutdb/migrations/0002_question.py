# Generated by Django 4.2.6 on 2024-04-16 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tutdb', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=255)),
                ('image', models.ImageField(blank=True, null=True, upload_to='question_images')),
                ('image_url', models.URLField(blank=True, null=True)),
                ('option_1', models.CharField(max_length=100)),
                ('option_2', models.CharField(max_length=100)),
                ('option_3', models.CharField(max_length=100)),
                ('option_4', models.CharField(max_length=100)),
                ('picked_answer', models.CharField(blank=True, max_length=1)),
                ('answer', models.CharField(max_length=1)),
                ('question_number', models.IntegerField()),
            ],
        ),
    ]
