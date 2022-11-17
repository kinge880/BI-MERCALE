# Generated by Django 4.0.4 on 2022-05-25 13:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='loginregister',
            options={'verbose_name_plural': 'Registro de logins'},
        ),
        migrations.AlterField(
            model_name='loginregister',
            name='userId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Usuário'),
        ),
        migrations.AlterField(
            model_name='loginregister',
            name='userIp',
            field=models.TextField(verbose_name='IP do usuário'),
        ),
        migrations.AlterField(
            model_name='loginregister',
            name='userLoginTime',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Data e hora do login'),
        ),
    ]
