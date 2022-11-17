# Generated by Django 4.0.4 on 2022-06-10 19:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('visions', '0005_vision_request_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='visions',
            name='linkVisionMobile',
            field=models.TextField(blank=True, default='', verbose_name='Url versão Mobile'),
        ),
        migrations.AlterField(
            model_name='vision_request',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Data e hora da solicitação'),
        ),
        migrations.AlterField(
            model_name='vision_request',
            name='status',
            field=models.CharField(default='Pendente', max_length=255, verbose_name='Status'),
        ),
    ]