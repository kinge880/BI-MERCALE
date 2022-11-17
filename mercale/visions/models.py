from django.db import models
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.core.exceptions import ValidationError, ObjectDoesNotExist, MultipleObjectsReturned

class visions(models.Model):
    
    nameVision = models.CharField(max_length = 255, verbose_name="Relatório")
    description = models.TextField(verbose_name="Descrição")
    linkVision = models.TextField(verbose_name="Url do PowerBI")
    linkVisionMobile = models.TextField(default='', blank=True, verbose_name="Url versão Mobile")
    is_active = models.BooleanField(default = True, verbose_name="É ativo?")
    created_at = models.DateTimeField(auto_now_add = True, verbose_name="Data de criação")
    updated_at = models.DateTimeField(auto_now = True, verbose_name="última edição")
    
    class Meta:
        verbose_name_plural = "Relatórios"
        verbose_name = 'Relatório' 
    def __str__(self):
        return self.nameVision
    
    def clean(self):
        if self.id == "none":  #Se o id for none significa que é um novo relatório, então ele valida apenas se os campos já existem
            if visions.objects.filter(nameVision=self.nameVision).exists():
                raise ValidationError('Já existe um relatório com esse nome!')
            elif visions.objects.filter(linkVision=self.linkVision).exists():
                raise ValidationError('Já existe um relatório com esse link!')
        else: #se existir um id, significa que estou editando um relatório, então faço validações extras
            try:
                testeName = visions.objects.get(nameVision=self.nameVision)
                if testeName.id != self.id:
                    raise ValidationError('Já existe um relatório com esse nome!')
            except MultipleObjectsReturned:
                raise ValidationError('Já existe um relatório com esse nome!')
            except ObjectDoesNotExist:
                pass
            
            try:
                testeLink = visions.objects.get(linkVision=self.linkVision)
                if testeLink.id != self.id:
                    raise ValidationError('Já existe um relatório com esse link!')
            except MultipleObjectsReturned:
                raise ValidationError('Já existe um relatório com esse link!')
            except ObjectDoesNotExist:
                pass           
            
    def save(self, *args, **kwargs):
        try:
            self.clean()
            super(visions, self).save(*args, **kwargs)
        except ValidationError as e:
            messages.add_message(e, messages.INFO, 'error!')
        except ObjectDoesNotExist:
            super(visions, self).save(*args, **kwargs)

class vision_to_user(models.Model):
    userId = models.ForeignKey(get_user_model(), verbose_name="Usuário", on_delete=models.CASCADE)
    visionId = models.ForeignKey(visions, verbose_name="Relatório", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True, verbose_name="Data de liberação")
    updated_at = models.DateTimeField(auto_now = True, verbose_name="última edição")
    
    class Meta:
        verbose_name_plural = "Liberação de relatórios"
        verbose_name = 'Liberação de relatório'    
    def __str__(self):
        return f'Usuário: {self.userId} | Relatório: {self.visionId}'
    
    def clean(self):
        if vision_to_user.objects.filter(userId=self.userId, visionId = self.visionId).exists():
            raise ValidationError('Esse usuário já recebeu acesso a esse relatório')
  
    def save(self, *args, **kwargs):
        try:
            self.clean()
            super(vision_to_user, self).save(*args, **kwargs)
        except ValidationError as e:
            messages.add_message(e, messages.INFO, 'Esse relatório já foi anexado ao usuário selecionado')
    
    def clean_admin(self):
        if vision_to_user.objects.filter(userId=self.userId, visionId = self.visionId).exists():
            raise ValidationError('Esse usuário já recebeu acesso a esse relatório')
    
    def save_admin_panel(self, *args, **kwargs):
            self.clean_admin()
            super(vision_to_user, self).save(*args, **kwargs)
            
class vision_request(models.Model):
    userId = models.ForeignKey(get_user_model(), verbose_name="Usuário solicitante", on_delete=models.CASCADE)
    visionId = models.ForeignKey(visions, verbose_name="Relatório solicitado", on_delete=models.CASCADE)
    description = models.TextField(verbose_name="Motivo da solicitação")
    status = models.CharField(max_length = 255, verbose_name="Status", default="Pendente")
    created_at = models.DateTimeField(auto_now_add = True, verbose_name="Data e hora da solicitação")
    updated_at = models.DateTimeField(auto_now = True, verbose_name="última edição")
    
    class Meta:
        verbose_name_plural = "Solicitação de relatórios"
        verbose_name = 'Solicitação de relatório'    
    def __str__(self):
        return f'Usuário solicitante: {self.userId} | Relatório solicitado: {self.visionId}'
    
    def clean(self):
        
        if vision_to_user.objects.filter(userId=self.userId, visionId = self.visionId).exists():
            raise ValidationError('você já recebeu acesso a esse relatório')
        if vision_request.objects.filter(userId=self.userId, visionId = self.visionId).exists():
            queryset = vision_request.objects.filter(userId=self.userId, visionId = self.visionId)
            for query in queryset:   
                if query.status == "Pendente":
                    raise ValidationError('você já solicitou acesso a esse relatório!')
  
    def save(self, *args, **kwargs):
        self.clean()
        super(vision_request, self).save(*args, **kwargs)