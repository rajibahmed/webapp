from fabric.api import env
from fabric.api import *

from fabric.contrib import files
from datetime import datetime

def setup():
    ssh()
    hostconfig()

def prod():
    env.hosts = ['10.100.0.70',]
    env.remote_admin = 'sysadmin'

def dev():
    env.hosts = ['172.16.195.11']
    env.remote_admin = 'rajib'


def ssh():
    for host in env.hosts:
        local("ssh-copy-id %s@%s" % (env.remote_admin, host))


def hostconfig():
    apt_upgrade()
    install_git()
    install_nodejs()
    install_nginx()

def cmd_exists(cmd):
    return files.exists("/usr/bin/%s" % cmd)


#######################
# Server initialization
#######################

def apt_upgrade():
    apt("upgrade")

def apt_update():
    apt("update -y")

def apt(cmd):
    sudo("apt-get %s" % cmd)

def install_git():
    if not cmd_exists('git'):
        apt("install -y git-core")
        run("git config --global color.ui true")

def install_nodejs():
    if not cmd_exists('nodejs'):
        apt("install -y nodejs")
        apt("install -y npm")

def install_nginx():
    if not cmd_exists('nginx'):
        apt("install -y nginx")
        put('default.nginx', '/etc/nginx/sites-available/default',use_sudo=True)

def install_goaccess():
    if not cmd_exists('goaccess'):
        apt("install -y goaccess")

#######################
# Code deployment
#######################

def start():
    with cd('/var/www/html/server'):
        run('nodejs index.js &')
    
    run('nginx -s reload')

def stop():
    sudo("killall nodejs")


def pack():
    local('tar -zcvf /tmp/app.tar.gz dist')
    run('rm /tmp/app.tar.gz')
    put("/tmp/app.tar.gz","/tmp/app.tar.gz")

def backup():
    if files.exists('/var/www/html'):
        run('tar -zcvf ~/%s.tar.gz /var/www/html/' % datetime.now().strftime('%Y%m%d%H%M%S'))

def deploy():
    pack()
    backup()

    with cd('/var/www/'):
        sudo('rm -rf html')
        sudo('tar -xzvf /tmp/app.tar.gz')
        sudo('mv dist html')


def add_cron():
    put('status_check.sh', '~/status_check.sh')
    run('crontab -l > /tmp/crondump')
    run('echo "* * * * *  ~/status_check.sh> /dev/null" >> /tmp/crondump')
    run('crontab /tmp/crondump')

