# Generated by Django 4.0.1 on 2024-05-17 02:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tutdb', '0003_choice_userscore_userresponse'),
    ]

    operations = [
        migrations.AddField(
            model_name='userresponse',
            name='course',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='tutdb.course'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userresponse',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default='2024-05-1 12:00:01'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userresponse',
            name='session',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='tutdb.session'),
            preserve_default=False,
        ),
    ]
