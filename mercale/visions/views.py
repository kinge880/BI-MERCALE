from django.shortcuts import render, redirect
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.template.loader import render_to_string
from .models import vision_to_user, visions, vision_request
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.contrib import messages

@login_required
def powerbi(request):
    user = request.user
    categorys = vision_to_user.objects.filter(userId_id = user.id)
    is_request = vision_request.objects.filter(status = 'Pendente')
    
    return render(request, 'visions/visionImplement/home.html', {'categorys': categorys, 'user': user, 'is_request' : is_request})

@login_required
def requestBi(request):
    user = request.user
    list = vision_to_user.objects.filter(userId_id = user.id).values_list('visionId_id', flat=True)
    requestvision = visions.objects.all().exclude(id__in = list)
    list_request = vision_request.objects.filter(userId_id = user.id)
    #define qual campo vai estar ativo
    #paginação
    paginator = Paginator(list_request, 10)
    page = request.GET.get('page')
    list_request_paginator = paginator.get_page(page)
    state = 1
    
    if request.method == 'POST':
            relatoryd = request.POST['relatory']
            vision_Idd = visions.objects.get(id = relatoryd)
            descriptionn = request.POST['reason']
            
            newRequest = vision_request(userId = user, description = descriptionn, visionId = vision_Idd)
            try:
                newRequest.save()
            except ValidationError as e:
                messages.error(request, e)
                state = 0
                return render(request, 'requestBi/requestBi.html', {'form_request': requestvision,'list_request': list_request_paginator, 'state':state})
            messages.success(request, 'Relatório solicitado com sucesso.')
            
            #recarrega a tabela
            state = 1
            paginator = Paginator(list_request, 10)
            page = request.GET.get('page')
            list_request_paginator = paginator.get_page(page)
            
            #envia email para a equipe de TI
            subject = "Nova solicitação de relatório"
            email_template_name = "requestBi/requestbi.txt"
            c = {
            "email": 'ti@mercale.com.br',
            'domain': 'mercalepowerbi.sa-east-1.elasticbeanstalk.com',
            'site_name': 'Mercale Power Bi',
            "user": user,
            'protocol': 'http',
            }
            email = render_to_string(email_template_name, c)
            try:
                send_mail(subject, email, 'admin@example.com',
                            ['ti@mercale.com.br'], fail_silently=False)
            except BadHeaderError:
                return render(request, 'requestBi/requestBi.html', {'form_request': requestvision,'list_request': list_request_paginator, 'state':state})    
            return render(request, 'requestBi/requestBi.html', {'form_request': requestvision,'list_request': list_request_paginator, 'state':state})
    else:
        return render(request, 'requestBi/requestBi.html', {'form_request': requestvision,'list_request': list_request_paginator, 'state':state})

