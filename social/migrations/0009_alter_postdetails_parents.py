# Generated by Django 4.0.1 on 2022-04-07 05:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0008_alter_postdetails_parents'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postdetails',
            name='parents',
            field=models.ForeignKey(blank=True, default=0, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='sub_comment', to='social.postdetails'),
        ),
    ]