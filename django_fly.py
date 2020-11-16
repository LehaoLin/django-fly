import click
import os
import sys
import platform


def check_environment():
    # Check OS
    if platform.system() == 'Linux':
        print("✅ This is a Linux server.")
    else:
        print("\033[0;31;40m❌ [Warning] This is not a Linux server. Aborting...\033[0m")
        sys.exit()

    # Check Django version
    try:
        import django
    except:
        print("⤵️ [Warning] Django is not detected. Django 2.2.13 will be installed...")
        os.system("sudo pip3 install django==2.2.13")
        # print("You can install NGINX by 'pip3 install django==2.2.13'")
    else:
        if list(django.VERSION)[0] != 2:
            print("\033[0;31;40m❌ [Warning] Sorry, Django-fly just provide service for Django 2.2.x at the current version.\033[0m")
            print("If you want to Django-fly be able for Django 3.x, please wait for new version or join us to be a contributor. https://github.com/LehaoLin/django-fly")
            sys.exit()

    # Check NGINX
    if not os.path.exists('/etc/nginx/'):
        print("\033[0;31;40m❌ [Warning] NGINX is not detected. Aborting...\033[0m")
        print("You can install NGINX by 'sudo apt install nginx'")
        sys.exit()
    
    # Check gunicorn
    try:
        import gunicorn
    except:
        print("\033[0;33;40m⤵️ [Warning] Gunicorn is not detected. Gunicorn will be installed...\033[0m")
        os.system("sudo pip3 install gunicorn")

    # Check supervisor
    try:
        import supervisor
    except:
        print("\033[0;33;40m⤵️ [Warning] Supervisor is not detected. Supervisor will be installed...\033[0m")
        os.system("sudo pip3 install supervisor")


def init_nginx_section(present_path):
    os.system(f"mkdir {present_path}/__deploy__/nginx_config")
    nginx_file_name = f'{present_path}/__deploy__/nginx_config/default.nginx'

    with open(nginx_file_name, 'w') as nginx_file_object:
        nginx_file_object.write('''server{
    listen 80;
    location /media {
    root /var/default;
    }
    location /static {{
    root /var/default;
    }
    location / {
    proxy_pass http://127.0.0.1:8000; 
    }
}''')


def init_supervisor_section(present_path):
    os.system(f"mkdir {present_path}/__deploy__/supervisor_config")
    supervisor_file_name = f'{present_path}/__deploy__/supervisor_config/default.conf'

    with open(supervisor_file_name, 'w') as supervisor_file_object:
        supervisor_file_object.write('''[program: default]
command = gunicorn [django project name].wsgi_prod -b 127.0.0.1:8000 -w 3
directory = [django project location]
autostart = true
autorestart = true        
''')


def update_nginx(present_path):
    nginx_dir = f'{present_path}/__deploy__/nginx_config'
    nginx_file_list = os.listdir(nginx_dir)
    for file in nginx_file_list:
        if str(file) == 'default.nginx':
            continue
        os.system(f"cp {nginx_dir}/{file} /etc/nginx/sites-available/")
        
        if os.path.exists(f'/etc/nginx/sites-enabled/{file}'):
            os.system(f"rm /etc/nginx/sites-enabled/{file}")
        
        os.system(f"ln -s /etc/nginx/sites-available/{file} /etc/nginx/sites-enabled/")
    
    os.system("service nginx restart")


def update_supervisor(present_path):
    supervisor_dir = f'{present_path}/__deploy__/supervisor_config'
    supervisor_file_list = os.listdir(supervisor_dir)
    for file in supervisor_file_list:
        if str(file) == 'default.conf':
            continue
        os.system(f"cp {supervisor_dir}/{file} /etc/supervisor/conf.d/")
    
    os.system("supervisorctl reload")




@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    if ctx.invoked_subcommand is None:
        print("\033[0;33;40mDjango-fly installed. Version 0.0.1\033[0m")
        print("\033[0;33;40mIf you want to initial the deploy section. 'django-fly init'\033[0m")
        print("\033[0;33;40mIf you want to update the deploy, 'django-fly update'\033[0m")


@cli.command()
def init():

    check_environment()
    
    present_path = os.path.abspath(os.path.join(os.getcwd(), "."))
    # print(present_path)

    os.system("mkdir __deploy__")
    init_nginx_section(present_path)
    init_supervisor_section(present_path)
    print("")
    print("🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀")
    print("🚀The deploy section is initialized!!!!!!")
    print("🚀Move your NGINX files and supervisor config files to the '__deploy__/nginx_config/' and '__deploy__/supervisor_config/'")
    print("🚀And you can use 'django-fly update' to update your NGINX and supervisor settings!")
    print("🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀")

    # Check letsencrypt
    if not os.path.exists('/etc/letsencrypt/'):
        print("")
        print("\033[0;31;40m[Warning] Letsencrypt is not detected. We recommand Letsencrypt.\033[0m")
        print("https://letsencrypt.org/")
        print("It is a nonprofit Certificate Authority providing TLS certificates to websites.")
        print("You can install Letsencrypt by 'sudo pip3 install certbot'")


@cli.command()
def update():
    present_path = os.path.abspath(os.path.join(os.getcwd(), "."))
    if not os.path.exists(f'{present_path}/__deploy__'):
        print("\033[0;31;40mPlease use the command under the directory which has the '__deploy__' sub-dir.\033[0m")

    update_nginx(present_path)
    update_supervisor(present_path)
    print("\033[0;33;40mUpdate Complete!\033[0m")
    
