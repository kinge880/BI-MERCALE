from tabnanny import verbose
from django.db import models
from django.contrib.auth import get_user_model

class loginRegister(models.Model):
    
    userId= models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name="Usuário")
    userIp = models.TextField(verbose_name="IP do usuário")
    userLoginTime = models.DateTimeField(auto_now_add = True, verbose_name="Data e hora do login")
    
    class Meta:
        verbose_name_plural = "Registro de logins"
    def __str__(self):
        return f'Usuário: {self.userId}'
