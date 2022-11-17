from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib import auth
from .models import loginRegister
from django.shortcuts import render, redirect
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes


def login_redirect(request):
    if not request.user.is_authenticated:
        if(request.method == "POST"):
            user_login = request.POST['username']
            user_password = request.POST['password']
            user = auth.authenticate(
                username=user_login, password=user_password)
            if user is not None:
                if user.is_active:
                    auth.login(request, user)
                    user_ip = get_client_ip(request)
                    ip_capture = loginRegister.objects.create(
                        userId=User.objects.filter(username=user_login).first(), userIp=user_ip)
                    return redirect('/')
                else:
                    context = {"error": "Usuário desativado!"}
                    return render(request, 'registration/login.html', context)
            else:
                context = {"error": "Usuário ou senha invalidos"}
                return render(request, 'registration/login.html', context)
        else: return render(request, 'registration/login.html', {})
    else: return redirect('/')


def register_user(request):
    if not request.user.is_authenticated:
        if(request.method == "POST"):
            try:
                user_aux_email = User.objects.get(email=request.POST['email'].strip())
                if user_aux_email:
                    context = {"email_error": "Email já cadastrado no sistema"}
                    return render(request, 'registration/register.html', context)
            except User.DoesNotExist:
                try:
                    user_aux_username = User.objects.get(
                        username=request.POST['username'].strip())
                    if user_aux_username:
                        context = {
                            "user_error": "Login já cadastrado no sistema"}
                        return render(request, 'registration/register.html', context)
                except User.DoesNotExist:
                    user_first_name = request.POST['first_name']
                    user_last_name = request.POST['last_name']
                    user_email = request.POST['email']
                    user_login = request.POST['username']
                    user_password = request.POST['password']
                    user_first_name = user_first_name.strip()
                    user_last_name = user_last_name.strip()
                    user_email = user_email.strip()
                    user_login = user_login.strip()

                    newUser = User.objects.create_user(email=user_email,
                                                        first_name=user_first_name,
                                                        last_name=user_last_name,
                                                        username=user_login,
                                                        password=user_password)
                    newUser.save()
                    return redirect('/accounts/login')
        else: return render(request, 'registration/register.html', {})
    else: return redirect('/')


def get_client_ip(request):
    ip_formated = request.META.get('HTTP_X_FORWARDED_FOR')
    if ip_formated:
        ip = ip_formated.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Solicitação para troca de senha"
                    email_template_name = "registration/password_reset_email.txt"
                    c = {
					"email": user.email,
					'domain': 'mercalepowerbi.sa-east-1.elasticbeanstalk.com',
					'site_name': 'Mercale Power Bi',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
					}
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'admin@example.com',
						          [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    return redirect('/accounts/password_reset/done/')  
            else:
                context = {"email_error": "Email não existe no banco de dados"}
                return render(request, 'registration/password_reset.html', context) 
        else:
            context = {"email_error": "Email informado não existe no sistema"}
            return render(request, 'registration/password_reset.html', context) 
    
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="registration/password_reset.html", context={"password_reset_form":password_reset_form})