# Generated by Django 4.0.6 on 2022-07-17 10:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_meta_alter_user_options_alter_user_managers_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='current_round',
            field=models.IntegerField(default=1),
        ),
        migrations.DeleteModel(
            name='AccessTokens',
        ),
    ]
