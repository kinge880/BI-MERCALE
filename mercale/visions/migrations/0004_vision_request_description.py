# Generated by Django 4.0.4 on 2022-05-25 22:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('visions', '0003_alter_vision_to_user_options_alter_visions_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='vision_request',
            name='description',
            field=models.TextField(default=1, verbose_name='Motivo da solicitação'),
            preserve_default=False,
        ),
    ]
