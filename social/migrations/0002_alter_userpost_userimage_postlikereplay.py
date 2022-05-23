# Generated by Django 4.0.1 on 2022-04-05 08:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userpost',
            name='userImage',
            field=models.FileField(default=None, upload_to='image/'),
        ),
        migrations.CreateModel(
            name='PostLikeReplay',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('like', models.BooleanField(default=False)),
                ('comment', models.CharField(max_length=20, null=True)),
                ('parents', models.IntegerField(default=0)),
                ('view', models.IntegerField(null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ('userPost', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='social.userpost')),
            ],
        ),
    ]
