# Generated by Django 4.0.1 on 2022-04-06 07:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0007_alter_postdetails_comments'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postdetails',
            name='parents',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='sub_comment', to='social.postdetails'),
        ),
    ]
